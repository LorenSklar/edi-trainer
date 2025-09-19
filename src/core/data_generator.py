"""
Data Generator

Generates valid field values for EDI transactions based on YAML specifications.
Uses flexible core generators: random_string, faker_based, datetime_past/future.
"""

import faker
import random
import yaml
from datetime import datetime, timedelta
from pathlib import Path

# YAML caches - load once, use many times
field_specs_cache = None
character_sets_cache = None

# Initialize faker
fake = faker.Faker()

# Insurance providers with proper EDI abbreviations (all under 15 characters)
INSURANCE_PROVIDERS = [
    "BCBS", "AETNA", "CIGNA", "HUMANA", "KAISER",
    "ANTHEM", "UNITEDHEALTH", "MOLINA", "CENTENE", "WELLCARE",
    "INDEPENDENCE", "HIGHMARK", "EMBLEM", "HEALTHFIRST", "FIDELIS",
    "AMERIGROUP", "WELLPOINT", "HEALTHNET", "PREMERA", "REGENCE",
    "HARVARD PILGRIM", "TUFTS", "FALLON", "NEIGHBORHOOD", "COMMUNITY",
    "REGIONAL", "LOCAL HEALTH", "STATE HEALTH", "COUNTY", "CITY HEALTH",
    "BLUE CROSS", "BLUE SHIELD", "MEDICARE", "MEDICAID", "TRICARE",
    "WORKERS COMP", "AUTO INS", "LIFE INS", "WAGMO"
]

# EDI delimiter characters that must never appear in field values
EDI_DELIMITERS = "*~:>+^"

def validate_edi_field_value(value):
    """
    Validate and format EDI field value: uppercase, remove punctuation, remove delimiters.
    
    Args:
        value: The field value to validate
        
    Returns:
        str: The validated and formatted value
    """
    import re
    
    # Convert to uppercase
    value = value.upper()
    
    # Remove punctuation (keep only letters, numbers, and spaces)
    value = re.sub(r'[^\w\s]', ' ', value)
    
    # Remove EDI delimiters
    for delimiter in EDI_DELIMITERS:
        value = value.replace(delimiter, ' ')
    
    # Clean up multiple spaces
    value = ' '.join(value.split())
    
    return value

def load_character_sets():
    """Load and cache character sets from YAML file."""
    global character_sets_cache
    if character_sets_cache is None:
        yaml_path = Path(__file__).parent.parent / "data" / "character_sets.yaml"
        with open(yaml_path, 'r') as f:
            character_sets_cache = yaml.safe_load(f)
    return character_sets_cache

def random_string_generator(
    characterset="alphanumeric",
    min_length=1,
    max_length=10,
    valid_values=None
):
    """
    Core random string generator with character set and length constraints.
    
    Args:
        characterset: Character set to use (numeric, alpha, alphanumeric, printable, etc.)
        min_length: Minimum length of generated string
        max_length: Maximum length of generated string
        valid_values: If provided, randomly select from this list instead of generating
        
    Returns:
        str: Generated random string
    """
    # If valid_values provided, use them instead of generating
    if valid_values:
        return random.choice(valid_values)
    
    # Load character sets
    character_sets = load_character_sets()
    
    # Convert to safe character set to avoid EDI delimiters
    safe_characterset = convert_to_safe_characterset(characterset)
    chars = character_sets.get(safe_characterset, character_sets["alphanumeric"])
    
    # Generate random length within constraints
    target_length = random.randint(min_length, max_length)
    
    # Generate random string
    result = ''.join(random.choice(chars) for _ in range(target_length))
    
    # Validate and clean
    return validate_edi_field_value(result)

def pick_valid_value(field_designation):
    """
    Pick a random valid value from YAML field specifications.
    
    Args:
        field_designation: Field ID (e.g., "ISA01", "ISA03")
        
    Returns:
        str: Random valid value from the field's valid_values list
    """
    field_specs = load_field_specs()
    
    # Extract segment name from field designation (e.g., "ISA01" -> "ISA")
    segment_name = field_designation[:3]
    
    # Get field spec from nested structure
    if segment_name in field_specs and 'fields' in field_specs[segment_name]:
        field_spec = field_specs[segment_name]['fields'].get(field_designation, {})
        
        valid_values = field_spec.get("valid_values", [])
        if valid_values:
            # Weight "00" much higher for authorization/security qualifiers
            if field_designation in ["ISA01", "ISA03"] and "00" in valid_values:
                # 90% chance of "00", 5% each for other values
                weights = [0.9 if val == "00" else 0.05 for val in valid_values]
                return random.choices(valid_values, weights=weights)[0]
            else:
                return random.choice(valid_values)
        
        # Fallback to default if no valid_values
        return field_spec.get("default", "N/A")
    
    return "N/A"


def generate_field_value(field_designation, min_length=None, max_length=None):
    """
    Generate a field value based on YAML field specifications.
    Uses field_type to determine the appropriate generator.
    
    Args:
        field_designation: Field ID (e.g., "ISA06", "ISA08")
        min_length: Override min_length from YAML
        max_length: Override max_length from YAML
        
    Returns:
        str: Generated field value
    """
    field_specs = load_field_specs()
    
    # Extract segment name from field designation (e.g., "ISA06" -> "ISA")
    segment_name = field_designation[:3]
    
    # Get field spec from nested structure
    if segment_name in field_specs and 'fields' in field_specs[segment_name]:
        field_spec = field_specs[segment_name]['fields'].get(field_designation, {})
        
        # Use provided lengths or fall back to YAML specs
        field_min_length = min_length or field_spec.get("min_length", 1)
        field_max_length = max_length or field_spec.get("max_length", 50)
        
        # Get field type from YAML
        field_type = field_spec.get("field_type", "generic")
        
        # Generate based on field type
        if field_type in ["company_name", "insurance_provider"]:
            return random_faker_generator(field_type, field_min_length, field_max_length)
        elif field_spec.get("valid_values"):
            return pick_valid_value(field_designation)
        else:
            # Fallback to string generation
            characterset = field_spec.get("characterset", "alphanumeric")
            return random_string_generator(characterset, field_min_length, field_max_length)
    
    return "N/A"


def random_faker_generator(
    field_type,
    min_length=1,
    max_length=50,
    **kwargs
):
    """
    Core faker-based generator for realistic data.
    
    Args:
        field_type: Type of faker data to generate
        min_length: Minimum length constraint
        max_length: Maximum length constraint
        **kwargs: Additional parameters for specific faker methods
        
    Returns:
        str: Generated realistic data
    """
    # Map field types to faker methods
    faker_methods = {
        "company_name": lambda: fake.company(),
        "insurance_provider": lambda: random.choice(INSURANCE_PROVIDERS),
        "first_name": lambda: fake.first_name(),
        "last_name": lambda: fake.last_name(),
        "address": lambda: fake.street_address(),
        "phone_number": lambda: fake.phone_number(),
        "email": lambda: fake.email(),
        "city": lambda: fake.city(),
        "state": lambda: fake.state_abbr(),
        "zip_code": lambda: fake.zipcode(),
        "ssn": lambda: fake.ssn().replace('-', ''),
        "member_id": lambda: fake.bothify(text='??#######'),
        "group_number": lambda: fake.bothify(text='GRP####'),
        "policy_number": lambda: fake.bothify(text='POL#######'),
    }
    
    # Generate value using faker
    if field_type in faker_methods:
        value = faker_methods[field_type]()
    else:
        # Fallback to generic string generation
        return random_string_generator("alphanumeric", min_length, max_length)
    
    # Validate and clean
    value = validate_edi_field_value(value)
    
    # Apply length constraints
    if len(value) > max_length:
        value = value[:max_length]
    elif len(value) < min_length:
        # Pad with spaces if needed
        value = value.ljust(min_length, ' ')
    
    return value

def random_past_date_generator(
    format_type="YYMMDD",
    days_back=365 * 5,
    **kwargs
):
    """
    Core datetime generator for past dates.
    
    Args:
        format_type: Date format (YYMMDD, YYYYMMDD, HHMM, etc.)
        days_back: How many days back to generate from today
        **kwargs: Additional parameters
        
    Returns:
        str: Formatted past date/time
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    random_date = fake.date_between(start_date=start_date, end_date=end_date)
    
    return format_datetime(random_date, format_type)

def random_future_date_generator(
    format_type="YYMMDD",
    days_forward=365 * 2,
    **kwargs
):
    """
    Core datetime generator for future dates.
    
    Args:
        format_type: Date format (YYMMDD, YYYYMMDD, HHMM, etc.)
        days_forward: How many days forward to generate from today
        **kwargs: Additional parameters
        
    Returns:
        str: Formatted future date/time
    """
    start_date = datetime.now()
    end_date = start_date + timedelta(days=days_forward)
    random_date = fake.date_between(start_date=start_date, end_date=end_date)
    
    return format_datetime(random_date, format_type)


def random_time_generator(
    format_type="HHMM",
    **kwargs
):
    """
    Core time generator.
    
    Args:
        format_type: Time format (HHMM, HHMMSS, etc.)
        **kwargs: Additional parameters
        
    Returns:
        str: Formatted time
    """
    if format_type == "HHMM":
        return fake.time(pattern="%H%M")
    elif format_type == "HHMMSS":
        return fake.time(pattern="%H%M%S")
    else:
        # Default to HHMM
        return fake.time(pattern="%H%M")

def convert_to_safe_characterset(characterset):
    """Convert character set to safe version (removes EDI delimiters)."""
    safe_mapping = {
        "printable": "printable_safe",
        "extended": "extended_safe",
    }
    return safe_mapping.get(characterset, characterset)

def format_datetime(date_obj, format_type):
    """Format datetime object according to specified format."""
    format_mapping = {
        "YYMMDD": "%y%m%d",
        "YYYYMMDD": "%Y%m%d",
        "MMDDYY": "%m%d%y",
        "MMDDYYYY": "%m%d%Y",
        "DDMMYY": "%d%m%y",
        "DDMMYYYY": "%d%m%Y",
    }
    
    format_str = format_mapping.get(format_type, "%y%m%d")
    return date_obj.strftime(format_str)

def parse_segment_specs(raw_yaml):
    """
    Parse raw YAML data into structured format for efficient access.
    
    Args:
        raw_yaml: Raw YAML data loaded from file
        
    Returns:
        dict: Parsed and structured segment specifications
    """
    if not raw_yaml or 'segments' not in raw_yaml:
        return {}
    
    parsed_specs = {}
    for segment_name, segment_data in raw_yaml['segments'].items():
        parsed_specs[segment_name] = {
            'description': segment_data.get('description', ''),
            'validation_rules': segment_data.get('validation_rules', []),
            'fields': {}
        }
    
    # Parse field specifications from top-level 'fields' section
    if 'fields' in raw_yaml:
        for field_id, field_data in raw_yaml['fields'].items():
            # Determine which segment this field belongs to based on prefix
            segment_name = field_id[:3]  # e.g., "ISA01" -> "ISA"
            
            if segment_name in parsed_specs:
                parsed_specs[segment_name]['fields'][field_id] = {
                    'name': field_data.get('name', ''),
                    'purpose': field_data.get('purpose', ''),
                    'rules': field_data.get('rules', ''),
                    'characterset': field_data.get('characterset', ''),
                    'valid_values': field_data.get('valid_values', []),
                    'examples': field_data.get('examples', ''),
                    'min_length': field_data.get('min_length', 0),
                    'max_length': field_data.get('max_length', 0),
                    'field_type': field_data.get('field_type', 'generic'),
                    'common_errors': field_data.get('common_errors', []),
                    'error_scenarios': field_data.get('error_scenarios', []),
                    'required': field_data.get('required', False),
                    'position': field_data.get('position', 0),
                    'default': field_data.get('default', '')
                }
    
    return parsed_specs

def load_field_specs():
    """Load and cache all field specifications from all YAML files."""
    global field_specs_cache
    if field_specs_cache is None:
        field_specs_cache = {}
        
        # Load from all YAML files
        yaml_files = [
            "envelope_segment_specifications.yaml",
            "member_segment_specifications.yaml", 
            "coverage_segment_specifications.yaml"
        ]
        
        for yaml_file in yaml_files:
            yaml_path = Path(__file__).parent.parent / "data" / yaml_file
            if yaml_path.exists():
                with open(yaml_path, 'r') as f:
                    raw_yaml = yaml.safe_load(f)
                # Parse and merge into single cache
                parsed_specs = parse_segment_specs(raw_yaml)
                field_specs_cache.update(parsed_specs)
    
    return field_specs_cache

def generate_valid_value(field_designation):
    """
    Generate a valid value for a field based on its YAML specification.
    Uses flexible core generators based on field type and YAML data.
    
    Args:
        field_designation: e.g., "ISA01", "ISA06", "N101"
        
    Returns:
        str: Valid value for the field
    """
    field_specs = load_field_specs()
    
    # Parse segment and field from designation (e.g., "ISA01" -> segment="ISA", field="ISA01")
    segment_name = field_designation[:3]  # "ISA", "IEA", "NM1", etc.
    
    if segment_name not in field_specs or field_designation not in field_specs[segment_name]['fields']:
        # Fallback to default if field not found
        return "DEFAULT"
    
    field_spec = field_specs[segment_name]['fields'][field_designation]
    
    # Handle special cases first
    if field_designation == "ISA02":
        # Authorization info should be 10 spaces when no authorization
        return "          "
    elif field_designation == "ISA04":
        # Security info should be 10 spaces when no security
        return "          "
    elif field_designation in ["ISA06", "ISA08"]:
        # Company IDs should be right-padded to 15 characters (EDI standard)
        company_name = random_faker_generator("company_name", 1, 15)
        return company_name.rjust(15, ' ')
    elif field_designation in ["ISA11", "ISA16"]:
        # These fields ARE the delimiter characters - use original printable set
        return random_string_generator(
            characterset=field_spec.get("characterset", "printable"),
            min_length=field_spec.get("min_length", 1),
            max_length=field_spec.get("max_length", 1),
            valid_values=field_spec.get("valid_values", [])
        )
    
    # Route to appropriate core generator based on field type and YAML data
    field_type = field_spec.get("field_type", "generic")
    characterset = field_spec.get("characterset", "alphanumeric")
    min_length = field_spec.get("min_length", 1)
    max_length = field_spec.get("max_length", min_length)
    valid_values = field_spec.get("valid_values", [])
    examples = field_spec.get("examples", "")
    
    # Determine generator type based on field type and context
    if field_type in ["company_name", "first_name", "last_name", "address", "phone_number", "email", "city", "state", "zip_code", "ssn", "member_id", "group_number", "policy_number"]:
        return random_faker_generator(field_type, min_length, max_length)
    
    elif field_type == "date":
        # Determine date context based on field purpose or examples
        if any(keyword in examples.lower() for keyword in ["enrollment", "eligibility", "start", "begin"]):
            return random_past_date_generator("YYMMDD" if min_length == 6 else "YYYYMMDD")
        elif any(keyword in examples.lower() for keyword in ["end", "termination", "expiration"]):
            return random_future_date_generator("YYMMDD" if min_length == 6 else "YYYYMMDD")
        else:
            return random_past_date_generator("YYMMDD" if min_length == 6 else "YYYYMMDD", days_back=30)
    
    elif field_type == "time":
        return random_time_generator("HHMM" if min_length == 4 else "HHMMSS")
    
    else:
        # Default to random string generation
        return random_string_generator(characterset, min_length, max_length, valid_values)
