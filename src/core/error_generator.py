"""
Error Generator

Generates field-level and structural errors for EDI transactions.
Reads field specifications from YAML and generates appropriate errors.
"""

import faker
import random
import yaml
from pathlib import Path

# YAML caches - loaded once, used many times
field_specs_cache = None
character_sets_cache = None

# TODO: Error Generator Status
# ✅ COMPLETED: Generic error generator (generate_generic_error)
#   - YAML-driven character sets
#   - Invalid character tracking with specific character display
#   - Weight-based error type selection
#   - Safe fallbacks for edge cases
#   - Valid string modification (clipping/extending for wrong_length)
#   - Comprehensive test coverage
#
# 🔄 TODO: Faker error generator (generate_faker_error)
#   - Implement proper faker-based error generation
#   - Test with name, company, address field types
#   - Add test coverage
#
# 🔄 TODO: Date/time error generator (generate_datetime_error)
#   - Implement date/time specific error types
#   - Add proper weights for date/time fields
#   - Test coverage
#
# 🔄 TODO: Structural error generator (structural_error_generator)
#   - Implement segment-level structural errors
#   - Test coverage

def load_character_sets():
    """Load and cache character sets from YAML file."""
    global character_sets_cache
    if character_sets_cache is None:
        yaml_path = Path(__file__).parent.parent / "data" / "character_sets.yaml"
        with open(yaml_path, 'r') as f:
            character_sets_cache = yaml.safe_load(f)
    return character_sets_cache


def generate_random_value(characterset, length):
    """
    Generate a random string of specified length using the given character set.
    
    Args:
        characterset: Character set name (numeric, alpha, alphanumeric, printable, extended)
        length: Desired length of the string
        
    Returns:
        str: Random string of specified length
    """
    character_sets = load_character_sets()
    chars = character_sets.get(characterset, character_sets["alphanumeric"])  # Default to alphanumeric
    
    return ''.join(random.choice(chars) for _ in range(length))


def get_invalid_characters(characterset):
    """
    Get characters that are invalid for the given character set.
    Returns characters from extended set that are not in the current set.
    
    Args:
        characterset: Current character set name
        
    Returns:
        list: Characters that are invalid for this character set
    """
    character_sets = load_character_sets()
    
    # Get current character set
    current_chars = character_sets.get(characterset, character_sets["extended"])
    
    # Get extended character set (most permissive)
    extended_chars = character_sets["extended"]
    
    # Return characters that are in extended but not in current set
    invalid_chars = [char for char in extended_chars if char not in current_chars]
    
    # If no invalid chars found, return empty list
    if not invalid_chars:
        invalid_chars = []
    
    return invalid_chars


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
        
        # Parse field specifications
        if 'fields' in segment_data:
            for field_id, field_data in segment_data['fields'].items():
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


def field_error_generator(field_designation, field_spec, valid_string=None):
    """
    Generate field-level errors based on YAML field specifications.
    
    Args:
        field_designation: e.g., "ISA01", "ISA15", "N101" 
        field_spec: The field definition from YAML
        valid_string: Valid string to corrupt (optional, will generate if not provided)
    
    Returns:
        dict: error_info with error details
    """
    field_type = field_spec.get("field_type", "generic")
    
    # Route to appropriate error generator based on field type
    if field_type in ["company_name", "first_name", "last_name", "address", "phone_number"]:
        return generate_faker_error(field_designation, field_spec, valid_string)
    elif field_type in ["date", "time"]:
        return generate_datetime_error(field_designation, field_spec)
    else:
        # Default to generic for "generic" type and unknown types
        return generate_generic_error(field_designation, field_spec, valid_string)


def generate_generic_error(field_designation, field_spec, valid_string=None):
    """Generate errors for generic fields using character sets."""
    # Generate valid string if not provided (fallback behavior)
    if valid_string is None:
        characterset = field_spec.get("characterset", "alphanumeric")
        min_length = field_spec.get("min_length", 1)
        max_length = field_spec.get("max_length", min_length)
        target_length = random.randint(min_length, max_length)
        valid_string = generate_random_value(characterset, target_length)
    
    # Weighted error types for generic fields
    error_types = {
        "blank_value": 10,      # String of spaces
        "missing_value": 15,    # Empty string
        "invalid_value": 25,    # Most common error type
        "invalid_character": 5, # Less common error type
        "wrong_format": 0,      # Not relevant for generic fields
        "wrong_length": 5       # Less common error type
    }
    
    # Pick error type
    error_type = random.choices(list(error_types.keys()), weights=list(error_types.values()))[0]
    
    # Generate specific error based on type
    if error_type == "blank_value":
        # Generate string of spaces of correct length
        min_length = field_spec.get("min_length", 1)
        max_length = field_spec.get("max_length", min_length)
        target_length = random.randint(min_length, max_length)
        blank_value = " " * target_length
        
        return {
            "error_type": "blank_value",
            "error_value": blank_value,
            "error_explanation": f"Required field {field_designation} is blank"
        }
    
    elif error_type == "missing_value":
        return {
            "error_type": "missing_value",
            "error_value": "",
            "error_explanation": f"Required field {field_designation} is missing"
        }
    
    elif error_type == "invalid_value":
        # 1) Use common_errors if present
        common_errors = field_spec.get("common_errors", [])
        if common_errors:
            invalid_value = random.choice(common_errors)
        
        # 2) Generate invalid value if valid_values present
        elif field_spec.get("valid_values"):
            valid_values = field_spec.get("valid_values", [])
            characterset = field_spec.get("characterset", "alphanumeric")
            min_length = field_spec.get("min_length", 1)
            max_length = field_spec.get("max_length", min_length)
            target_length = random.randint(min_length, max_length)
            
            # Generate random value until we get one not in valid_values
            max_attempts = 100
            for _ in range(max_attempts):
                invalid_value = generate_random_value(characterset, target_length)
                if invalid_value not in valid_values:
                    break
            else:
                # Fallback if we can't generate a unique invalid value
                invalid_value = "N/A"
        
        # 3) Fallback to "N/A" if neither present
        else:
            invalid_value = "N/A"
        
        return {
            "error_type": "invalid_value",
            "error_value": invalid_value,
            "error_explanation": f"Invalid value '{invalid_value}' for {field_designation}"
        }
    
    elif error_type == "invalid_character":
        characterset = field_spec.get("characterset", "alphanumeric")
        
        # Get invalid characters from extended set but not in current set
        invalid_chars = get_invalid_characters(characterset)
        
        # If no invalid characters available, fallback to missing_value
        if not invalid_chars:
            return {
                "error_type": "missing_value",
                "error_value": "",
                "error_explanation": f"Required field {field_designation} is missing"
            }
        
        # Assume valid_string is passed in - corrupt it with invalid characters
        # Pick 1-3 positions to corrupt
        corrupt_count = random.randint(1, 3)
        corrupt_positions = [random.randint(0, len(valid_string) - 1) for _ in range(corrupt_count)]
        
        # Corrupt the string and track which characters were used
        corrupted_string = list(valid_string)
        used_invalid_chars = []
        for pos in corrupt_positions:
            invalid_char = random.choice(invalid_chars)
            corrupted_string[pos] = invalid_char
            if invalid_char not in used_invalid_chars:
                used_invalid_chars.append(invalid_char)
        
        invalid_value = ''.join(corrupted_string)
        
        # Create explanation with specific invalid characters
        invalid_chars_str = ', '.join(f"'{char}'" for char in used_invalid_chars)
        explanation = f"Invalid character(s) {invalid_chars_str} in {field_designation} not in {characterset} set"
        
        return {
            "error_type": "invalid_character",
            "error_value": invalid_value,
            "error_explanation": explanation
        }
    
    elif error_type == "wrong_length":
        min_len = field_spec.get("min_length", 1)
        max_len = field_spec.get("max_length", 10)
        characterset = field_spec.get("characterset", "alphanumeric")
        
        # Generate wrong length (too short or too long)
        wrong_len = random.choice([min_len - 1, max_len + 1])
        
        if wrong_len < len(valid_string):
            # Too short: clip the valid string
            wrong_value = valid_string[:wrong_len]
        else:
            # Too long: extend the valid string with valid characters
            character_sets = load_character_sets()
            chars = character_sets.get(characterset, character_sets["alphanumeric"])
            extension = ''.join(random.choice(chars) for _ in range(wrong_len - len(valid_string)))
            wrong_value = valid_string + extension
        
        return {
            "error_type": "wrong_length",
            "error_value": wrong_value,
            "error_explanation": f"Wrong length {len(wrong_value)} for {field_designation} (expected {min_len}-{max_len})"
        }
    
    else:
        # Fallback for any unexpected error types
        return {
            "error_type": "missing_value",
            "error_value": "",
            "error_explanation": f"Required field {field_designation} is missing"
        }


def generate_faker_error(field_designation, field_spec, valid_string=None):
    """Generate errors for faker-based fields (names, addresses, etc.)."""
    fake = Faker()
    field_type = field_spec.get("field_type")
    
    # Generate valid string if not provided (fallback behavior)
    if valid_string is None:
        if field_type == "name":
            valid_string = fake.name()
        elif field_type == "company":
            valid_string = fake.company()
        elif field_type == "address":
            valid_string = fake.street_address()
        else:
            # Default to generic generation
            characterset = field_spec.get("characterset", "alphanumeric")
            min_length = field_spec.get("min_length", 1)
            max_length = field_spec.get("max_length", min_length)
            target_length = random.randint(min_length, max_length)
            valid_string = generate_random_value(characterset, target_length)
    
    # Weighted error types for faker fields
    error_types = {
        "blank_value": 10,      # String of spaces of correct length
        "missing_value": 15,    # Empty string (field absent)
        "invalid_value": 20,
        "wrong_format": 25,
        "wrong_length": 20,
        "invalid_character": 20
    }
    
    error_type = random.choices(list(error_types.keys()), weights=list(error_types.values()))[0]
    
    if error_type == "blank_value":
        # Generate string of spaces of correct length
        min_length = field_spec.get("min_length", 1)
        max_length = field_spec.get("max_length", min_length)
        target_length = random.randint(min_length, max_length)
        blank_value = " " * target_length
        
        return {
            "error_type": "blank_value",
            "error_value": blank_value,
            "error_explanation": f"Required field {field_designation} contains only spaces"
        }
    
    elif error_type == "missing_value":
        return {
            "error_type": "missing_value",
            "error_value": "",
            "error_explanation": f"Required field {field_designation} is missing"
        }
    
    elif error_type == "invalid_value":
        # 1) Use common_errors if present
        common_errors = field_spec.get("common_errors", [])
        if common_errors:
            invalid_value = random.choice(common_errors)
        
        # 2) Generate invalid value if valid_values present
        elif field_spec.get("valid_values"):
            valid_values = field_spec.get("valid_values", [])
            characterset = field_spec.get("characterset", "alphanumeric")
            min_length = field_spec.get("min_length", 1)
            max_length = field_spec.get("max_length", min_length)
            target_length = random.randint(min_length, max_length)
            
            # Generate random value until we get one not in valid_values
            max_attempts = 100
            for _ in range(max_attempts):
                invalid_value = generate_random_value(characterset, target_length)
                if invalid_value not in valid_values:
                    break
            else:
                # Fallback if we can't generate a unique invalid value
                invalid_value = "N/A"
        
        # 3) Fallback to "N/A" if neither present
        else:
            invalid_value = "N/A"
        
        return {
            "error_type": "invalid_value",
            "error_value": invalid_value,
            "error_explanation": f"Invalid value '{invalid_value}' for {field_designation}"
        }
    
    elif error_type == "wrong_format":
        return {
            "error_type": "wrong_format",
            "error_value": invalid_value,
            "error_explanation": f"Wrong format for {field_designation}"
        }
    
    elif error_type == "wrong_length":
        min_len = field_spec.get("min_length", 1)
        max_len = field_spec.get("max_length", 10)
        wrong_len = random.choice([min_len - 1, max_len + 1])
        
        return {
            "error_type": "wrong_length",
            "error_value": invalid_value,
            "error_explanation": f"Wrong length {wrong_len} for {field_designation} (expected {min_len}-{max_len})"
        }
    
    elif error_type == "invalid_character":
        characterset = field_spec.get("characterset", "alphanumeric")
        
        # Get invalid characters from extended set but not in current set
        invalid_chars = get_invalid_characters(characterset)
        
        # If no invalid characters available, fallback to missing_value
        if not invalid_chars:
            return {
                "error_type": "missing_value",
                "error_value": "",
                "error_explanation": f"Required field {field_designation} is missing"
            }
        
        # Corrupt valid_string with invalid characters
        # Pick 1-3 positions to corrupt
        corrupt_count = random.randint(1, 3)
        corrupt_positions = [random.randint(0, len(valid_string) - 1) for _ in range(corrupt_count)]
        
        # Corrupt the string and track which characters were used
        corrupted_string = list(valid_string)
        used_invalid_chars = []
        for pos in corrupt_positions:
            invalid_char = random.choice(invalid_chars)
            corrupted_string[pos] = invalid_char
            if invalid_char not in used_invalid_chars:
                used_invalid_chars.append(invalid_char)
        
        invalid_value = ''.join(corrupted_string)
        
        # Create explanation with specific invalid characters
        invalid_chars_str = ', '.join(f"'{char}'" for char in used_invalid_chars)
        explanation = f"Invalid character(s) {invalid_chars_str} in {field_designation} (not in {characterset} set)"
        
        return {
            "error_type": "invalid_character",
            "error_value": invalid_value,
            "error_explanation": explanation
        }


def generate_datetime_error(field_designation, field_spec):
    """Generate errors for date/time fields."""
    field_type = field_spec.get("field_type")
    
    # Weighted error types for date/time fields
    error_types = {
        "blank_value": 10,      # String of spaces of correct length
        "missing_value": 15,    # Empty string (field absent)
        "invalid_date": 25,
        "future_date": 15,
        "invalid_time": 25,
        "wrong_format": 20
    }
    
    error_type = random.choices(list(error_types.keys()), weights=list(error_types.values()))[0]
    
    if error_type == "blank_value":
        # Generate string of spaces of correct length
        min_length = field_spec.get("min_length", 1)
        max_length = field_spec.get("max_length", min_length)
        target_length = random.randint(min_length, max_length)
        blank_value = " " * target_length
        
        return {
            "error_type": "blank_value",
            "error_value": blank_value,
            "error_explanation": f"Required field {field_designation} contains only spaces"
        }
    
    elif error_type == "missing_value":
        return {
            "error_type": "missing_value",
            "error_value": "",
            "error_explanation": f"Required field {field_designation} is missing"
        }
    
    elif error_type == "invalid_date":
        return {
            "error_type": "invalid_date",
            "error_value": invalid_value,
            "error_explanation": f"Invalid date format for {field_designation}"
        }
    
    elif error_type == "future_date":
        return {
            "error_type": "future_date",
            "error_value": invalid_value,
            "error_explanation": f"Future date in {field_designation}"
        }
    
    elif error_type == "invalid_time":
        return {
            "error_type": "invalid_time",
            "error_value": invalid_value,
            "error_explanation": f"Invalid time format for {field_designation}"
        }
    
    elif error_type == "wrong_format":
        return {
            "error_type": "wrong_format",
            "error_value": invalid_value,
            "error_explanation": f"Wrong format for {field_designation}"
        }


def structural_error_generator():
    """
    Generate structural errors that affect segments or transaction structure.
    
    Returns:
        dict: error_info with structural error details
    """
    # Weighted structural error types
    error_types = {
        "control_number_mismatch": 30,
        "date_time_mismatch": 20,
        "missing_segment": 25,
        "extra_segment": 15,
        "wrong_segment_order": 10
    }
    
    error_type = random.choices(list(error_types.keys()), weights=list(error_types.values()))[0]
    
    if error_type == "control_number_mismatch":
        return {
            "error_type": "control_number_mismatch",
            "error_value": "MISMATCH",
            "error_field": None,
            "error_explanation": "ISA13 and IEA02 control numbers do not match"
        }
    
    elif error_type == "date_time_mismatch":
        return {
            "error_type": "date_time_mismatch",
            "error_value": "MISMATCH",
            "error_field": None,
            "error_explanation": "ISA09 date and ISA10 time are inconsistent"
        }
    
    elif error_type == "missing_segment":
        return {
            "error_type": "missing_segment",
            "error_value": "MISSING",
            "error_field": None,
            "error_explanation": "Required segment is missing"
        }
    
    elif error_type == "extra_segment":
        return {
            "error_type": "extra_segment",
            "error_value": "EXTRA",
            "error_field": None,
            "error_explanation": "Unexpected segment found"
        }
    
    elif error_type == "wrong_segment_order":
        return {
            "error_type": "wrong_segment_order",
            "error_value": "WRONG_ORDER",
            "error_field": None,
            "error_explanation": "Segments are in wrong order"
        }
