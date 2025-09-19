"""
Error Generator

Generates field-level and structural errors for EDI transactions.
Uses YAML-driven field specifications and individual error generators.

ERROR SCENARIOS FROM YAML:
Field-level errors:
- blank_value: Field contains only spaces
- missing_value: Field is empty
- invalid_value: Field value not in valid_values list (requires valid_values)
- invalid_character: Field contains characters not in allowed character set
- invalid_length: Field length outside min/max constraints
- invalid_date: Includes wrong length, wrong order, wrong format, invalid month, 
  invalid day, future date, and includes separators
- invalid_time: Time format errors (wrong length, wrong format, invalid hour, invalidminute)
- all_zeros: Field contains all zeros (common error for numeric fields)

Structural errors (future implementation):
- incorrect_group_count: Group count field doesn't match actual count
- incorrect_control_number: Control number doesn't match expected value
- incorrect_date: Date inconsistencies between related fields
- incorrect_time: Time inconsistencies between related fields
- missing_envelope: Required envelope is missing
- missing_segment: Required segment is missing
- missing_field: Required field is missing
- extra_field: Unexpected filed present
- wrong_delimiter: Wrong delimiter used
- wrong_terminator: Wrong terminator used
- missing_terminator: Missing terminator


PROTECTION: Generator defaults to missing_value or "N/A" if needed information is not available

TODO: Update blank_value_generator and missing_value_generator to handle both required and non-required fields

TODO: Implement faker-specific invalid_length_generator for fields that use faker data (names, addresses, etc.) - need to handle realistic length variations

COMPLETED: ✅ Error scenario weighting implemented using equal weights for MVP
NOTE: Currently using equal weights for all scenarios within a field because:
1. MVP simplicity - easier to test all error types equally
2. Scenario weighting can be added later when we have real production error data

TODO: Implement remaining error generators:

FIELD-LEVEL ERRORS:
- invalid_date_generator: For ISA09 (date) - wrong format, future dates, invalid dates
- invalid_time_generator: For ISA10 (time) - wrong format, invalid times
- invalid_character_generator using wrong character set for realism
  - More realistic than injecting single random bad characters
  - Developer misunderstanding requirements more likely than a typo or corrupt bit
  - Example: ISA06 alphanumeric but generated using expanded character set 

STRUCTURAL ERRORS (ISA/IEA specific):
- incorrect_count_generator: IEA01 count doesn't match actual functional group count
- incorrect_control_number_generator: IEA02 control number doesn't match ISA13
- incorrect_date_generator: ISA09 date doesn't match transaction date (structural error)
- incorrect_time_generator: ISA10 time doesn't match transaction time (structural error)
- missing_terminator_generator: Remove segment terminator (~) from ISA/IEA
- wrong_delimiter_generator: Use wrong delimiter characters (*) in ISA/IEA
- missing_segment: Required ISA or IEA segment is missing
- extra_segment: Add unexpected segments between ISA/IEA

GENERAL STRUCTURAL ERRORS:
- missing_field_generator: Remove required fields from segments
- extra_field_generator: Add unexpected fields to segments
- wrong_terminator_generator: Use wrong segment terminator
- missing_envelope: Required envelope is missing

TODO: Submit Python PR for str.join() final_joiner parameter:
    ", ".join(items, final_joiner=" or ")  # → "A, B or C"
    
NOTE: Finally, a valid argument against the Oxford comma! Can you see why?

"""

import random
import yaml
from pathlib import Path

# YAML caches - load once, use many times
field_specs_cache = None
character_sets_cache = None

def load_character_sets():
    """Load and cache character sets from YAML file."""
    global character_sets_cache
    if character_sets_cache is None:
        yaml_path = Path(__file__).parent.parent / "data" / "character_sets.yaml"
        with open(yaml_path, 'r') as f:
            character_sets_cache = yaml.safe_load(f)
    return character_sets_cache

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

def parse_segment_specs(raw_yaml):
    """Parse raw YAML data into structured format for efficient access."""
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
                    'error_weight': field_data.get('error_weight', 'rare'),
                    'required': field_data.get('required', False),
                    'position': field_data.get('position', 0),
                    'default': field_data.get('default', '')
                }
    
    return parsed_specs

# Field-level error generators
def blank_value_generator(field_designation, field_spec, valid_value, error_info=None):
    """Generate blank value error meaning spaces with required length."""
    min_length = field_spec.get("min_length", 1)
    max_length = field_spec.get("max_length", min_length)
    target_length = random.randint(min_length, max_length)
    blank_value = " " * target_length
    
    # Update error_info if provided
    if error_info is not None:
        error_info["error_type"] = "blank_value"
        error_info["error_value"] = blank_value
        error_info["error_explanation"] = f"{field_designation} is blank with spaces only"
    
    return blank_value
    
def missing_value_generator(field_designation, field_spec, valid_value, error_info=None):
    """Generate missing value error (empty string)."""
    # Update error_info if provided
    if error_info is not None:
        error_info["error_type"] = "missing_value"
        error_info["error_value"] = ""
        error_info["error_explanation"] = f"{field_designation} is missing"
    
    return ""
    
def invalid_value_generator(field_designation, field_spec, valid_value, error_info=None):
    """Generate invalid value error (value not in valid_values list)."""
    common_errors = field_spec.get("common_errors", [])
    valid_values = field_spec.get("valid_values", [])
    
    # Use common_errors if available
    if common_errors:
        invalid_value = random.choice(common_errors)
    # Generate random value that's not in valid_values
    elif valid_values:
        characterset = field_spec.get("characterset", "alphanumeric")
        min_length = field_spec.get("min_length", 1)
        max_length = field_spec.get("max_length", min_length)
        
        # Try to generate invalid value (limited attempts)
        max_attempts = 10
        for attempt in range(max_attempts):
            invalid_value = random_string_generator(characterset, min_length, max_length)
            if invalid_value not in valid_values:
                break
        else:
            # If we couldn't find a valid invalid value, use fallback
            invalid_value = "N/A"
    # Fallback protection
    else:
        invalid_value = "N/A"
        
    # Update error_info if provided
    if error_info is not None:
        error_info["error_type"] = "invalid_value"
        error_info["error_value"] = str(invalid_value)
        # Show valid values with elegant formatting using smart join
        def smart_join(items, final_joiner=" or "):
            """Join items with commas, using final_joiner before the last item."""
            if len(items) <= 1:
                return "".join(f"'{item}'" for item in items)
            return ", ".join(f"'{item}'" for item in items[:-1]) + f"{final_joiner}'{items[-1]}'"
        
        valid_list = smart_join(valid_values)
        
        error_info["error_explanation"] = f"{field_designation} contains invalid value '{invalid_value}' not {valid_list}"
    
    return str(invalid_value)
    
def invalid_character_generator(field_designation, field_spec, valid_value, error_info=None):
    """Generate invalid character error (characters not in allowed character set)."""
    characterset = field_spec.get("characterset", "alphanumeric")
        
    # Load character sets
    character_sets = load_character_sets()
    
    # Get unsafe characters from predefined unsafe character sets
    unsafe_charset_name = f"{characterset}_unsafe"
    unsafe_chars = character_sets.get(unsafe_charset_name, "")
    
    # Protection: if no unsafe chars defined or at extended level, use N/A
    if not unsafe_chars or characterset == "extended":
        return {
            "error_type": "invalid_character",
            "error_value": "N/A",
            "error_explanation": f"{field_designation} cannot generate invalid characters (at highest character set level)"
        }
    
    # Use the provided valid_value as base and inject unsafe characters
    result = str(valid_value)
    target_length = len(result)
    injected_chars = []
    
    # Add unsafe characters at random positions (heavily weight single character)
    if random.random() < 0.8:  # 80% chance of single character
        num_unsafe = 1
    elif random.random() < 0.95:  # 15% chance of two characters  
        num_unsafe = 2
    else:  # 5% chance of three characters
        num_unsafe = min(3, target_length)
    for _ in range(num_unsafe):
        pos = random.randint(0, target_length - 1)
        injected_char = random.choice(unsafe_chars)
        injected_chars.append(injected_char)
        result = result[:pos] + injected_char + result[pos + 1:]
        
    # Update error_info if provided
    if error_info is not None:
        error_info["error_type"] = "invalid_character"
        error_info["error_value"] = result
        # Show which specific invalid characters were injected
        chars_list = ", ".join(f"'{char}'" for char in set(injected_chars))
        error_info["error_explanation"] = f"{field_designation} contains invalid characters: {chars_list}"
    
    return result

def invalid_length_generator(field_designation, field_spec, valid_value, error_info=None):
    """Generate wrong length error (value outside min/max length constraints)."""
    min_length = field_spec.get("min_length", 1)
    max_length = field_spec.get("max_length", min_length)
    characterset = field_spec.get("characterset", "alphanumeric")
    
    # Load character sets for adding valid characters
    character_sets = load_character_sets()
    safe_characterset = convert_to_safe_characterset(characterset)
    allowed_chars = character_sets.get(safe_characterset, character_sets["alphanumeric"])
    
    # Use the provided valid_value as base
    result = str(valid_value)
    current_length = len(result)
    
    # Determine if we should make it too short or too long
    if random.random() < 0.5 and min_length > 1:
        # Too short - remove characters from the end
        target_length = random.randint(1, min_length - 1)
        result = result[:target_length]
    else:
        # Too long - add valid characters to the end
        target_length = max_length + random.randint(1, 5)
        extra_chars = ''.join(random.choice(allowed_chars) for _ in range(target_length - current_length))
        result = result + extra_chars
    
    # Update error_info if provided
    if error_info is not None:
        error_info["error_type"] = "invalid_length"
        error_info["error_value"] = result
        error_info["error_explanation"] = f"{field_designation} has wrong length {len(result)}, expected {min_length}-{max_length}"
    
    return result

def all_zeros_generator(field_designation, field_spec, valid_value, error_info=None):
    """Generate all zeros error for numeric fields."""
    min_length = field_spec.get("min_length", 1)
    max_length = field_spec.get("max_length", min_length)
    target_length = random.randint(min_length, max_length)
    error_value = "0" * target_length
    
    # Update error_info if provided
    if error_info is not None:
        error_info["error_type"] = "all_zeros"
        error_info["error_value"] = error_value
        error_info["error_explanation"] = f"{field_designation} contains all zeros, which is invalid"
    
    return error_value

# Helper functions
def random_string_generator(characterset, min_length, max_length):
    """Helper function to generate random strings with character set constraints."""
    character_sets = load_character_sets()
    safe_characterset = convert_to_safe_characterset(characterset)
    chars = character_sets.get(safe_characterset, character_sets["alphanumeric"])
    
    target_length = random.randint(min_length, max_length)
    return ''.join(random.choice(chars) for _ in range(target_length))

def convert_to_safe_characterset(characterset):
    """Convert character set to safe version (removes EDI delimiters)."""
    safe_mapping = {
        "printable": "printable_safe",
        "extended": "extended_safe",
    }
    return safe_mapping.get(characterset, characterset)

def convert_error_weight_to_rate(error_weight):
    """Convert semantic error weight to numeric error rate."""
    weight_mapping = {
        "very_common": 0.3,  # 30% chance of error
        "common": 0.1,       # 10% chance of error
        "rare": 0.02,        # 2% chance of error
        "never": 0.0         # 0% chance of error
    }
    return weight_mapping.get(error_weight, 0.02)  # Default to rare

def pick_random_field_for_error(segment_name):
    """Pick a random field from YAML specs for the given segment."""
    field_specs = load_field_specs()
    
    # Get all fields for this segment from nested structure
    segment_fields = []
    if segment_name in field_specs and 'fields' in field_specs[segment_name]:
        segment_fields = list(field_specs[segment_name]['fields'].keys())
    
    if not segment_fields:
        return None
    
    return random.choice(segment_fields)


def structural_error_generator(error_type="fallback", field_values=None, error_info=None):
    """Generate structural errors by modifying field_values list."""
    if field_values is None:
        field_values = []
    
    # Update error_info if provided (like field error generators)
    if error_info is not None:
        if error_type == "fallback":
            error_info["error_type"] = "missing_segment"
            error_info["error_value"] = ""  # Empty string = missing segment
            error_info["error_explanation"] = "Segment is missing (structural error fallback)"
        else:
            error_info["error_type"] = "missing_segment"
            error_info["error_value"] = ""  # Empty string = missing segment
            error_info["error_explanation"] = f"Structural error: {error_type} (implementation pending - fallback to missing segment)"
    
    # TODO: Implement actual structural error modifications:
    # - wrong_delimiter: Replace all "*" with "|" or other delimiters
    # - missing_terminator: Remove the final "~"
    # - extra_field: Add an extra field to the list
    # - missing_field: Remove a required field from the list
    
    # Return the modified segment value (empty string for missing segment)
    return ""

def is_error_in_field(field_designation, error_info):
    """Check if there is an error in this specific field based on error_info."""
    if not error_info:
        return False
    
    return (error_info.get("error_target") == "FIELD" and 
            error_info.get("error_field") == field_designation)

# Main error generation function
def field_error_generator(field_designation, field_spec, valid_value):
    """
    Generate field-level errors based on YAML specifications.
    
    Args:
        field_designation: Field identifier (e.g., "ISA01")
        field_spec: Field specification from YAML
        valid_value: Current valid value for the field
    
    Returns:
        dict: Error information with type, value, and explanation
    """
    error_scenarios = field_spec.get("error_scenarios", [])
    
    if not error_scenarios:
        # No error scenarios defined, return valid value
        return {
            "error_type": "none",
            "error_value": valid_value,
            "error_explanation": f"No error scenarios defined for {field_designation}"
        }
    
    # Choose random error scenario
    error_type = random.choice(error_scenarios)
    
    # Route to appropriate generator
    generator_map = {
        "blank_value": blank_value_generator,
        "missing_value": missing_value_generator,
        "invalid_value": invalid_value_generator,
        "invalid_character": invalid_character_generator,
        "invalid_length": invalid_length_generator,
        "all_zeros": all_zeros_generator,
    }
    
    generator = generator_map.get(error_type)
    if generator:
        return generator(field_designation, field_spec, valid_value)
    else:
        # Fallback for unimplemented error types
        return {
            "error_type": "fallback",
            "error_value": "N/A",
            "error_explanation": f"Error type '{error_type}' not implemented for {field_designation}"
        }