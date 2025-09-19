"""
Envelope Segment Generator

Generates envelope/structural segments and their field generators for EDI 834 transactions.
Handles all structural segments: ISA, IEA, GS, GE, ST, SE, BGN.
"""

from .error_generator import load_field_specs, is_error_in_field, blank_value_generator, missing_value_generator, invalid_value_generator, invalid_character_generator, invalid_length_generator, all_zeros_generator
from .data_generator import (
    random_string_generator, random_faker_generator, 
    random_past_date_generator, random_future_date_generator, 
    random_time_generator, pick_valid_value,
    load_character_sets, convert_to_safe_characterset
)
import random
import yaml
from pathlib import Path

# Weight constants for valid value selection
MOST_COMMON_WEIGHT = 0.9
LESS_COMMON_WEIGHT = 0.05

# YAML cache - load once, use many times
field_specs_cache = None

def apply_field_error(field_designation, field_spec, valid_value, error_info=None):
    """
    Apply error to a field based on its YAML error scenarios.
    
    Args:
        error_info: Shared state dict - gets updated with error details (error_type, error_value, error_explanation)
                   Returns just the error value, not the full dict.
    """
    error_scenarios = field_spec.get("error_scenarios", ["missing_value"])
    error_type = random.choice(error_scenarios)
    
    # Call the right error generator - they update error_info directly
    if error_type == "blank_value":
        return blank_value_generator(field_designation, field_spec, valid_value, error_info)
    elif error_type == "missing_value":
        return missing_value_generator(field_designation, field_spec, valid_value, error_info)
    elif error_type == "invalid_value":
        return invalid_value_generator(field_designation, field_spec, valid_value, error_info)
    elif error_type == "invalid_character":
        return invalid_character_generator(field_designation, field_spec, valid_value, error_info)
    elif error_type == "invalid_length":
        return invalid_length_generator(field_designation, field_spec, valid_value, error_info)
    elif error_type == "all_zeros":
        return all_zeros_generator(field_designation, field_spec, valid_value, error_info)
    elif error_type == "mismatch_control_number":
        # Fallback case - update error_info here
        if error_info is not None:
            error_info["error_type"] = "mismatch_control_number"
            error_info["error_value"] = "999999999"
            error_info["error_explanation"] = "Control number mismatch (TODO: implement this structural error)"
        return "999999999"
    elif error_type in ["invalid_date", "invalid_time"]:
        # Fallback case - update error_info here
        if error_info is not None:
            error_info["error_type"] = error_type
            error_info["error_value"] = "N/A"
            error_info["error_explanation"] = f"TODO: Implement {error_type} error generator"
        return "N/A"
    else:
        # Fallback case - update error_info here
        if error_info is not None:
            error_info["error_type"] = "unknown"
            error_info["error_value"] = "N/A"
            error_info["error_explanation"] = "Unknown error type (fallback)"
        return "N/A"

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
                from .error_generator import parse_segment_specs
                parsed_specs = parse_segment_specs(raw_yaml)
                field_specs_cache.update(parsed_specs)
    
    return field_specs_cache

#=============================================================================
# ISA SEGMENT
#=============================================================================

# ISA Field Generators
def generate_authorization_qualifier(error_target=None, error_info=None):
    """Generate ISA01 - Authorization Information Qualifier"""
    # Generate valid value first
    field_specs = load_field_specs()
    field_spec = field_specs["ISA"]["fields"]["ISA01"]
    valid_values = field_spec.get("valid_values", [])
    # "00" most common authorization qualifier
    if "00" in valid_values:
        weights = [MOST_COMMON_WEIGHT if val == "00" else LESS_COMMON_WEIGHT for val in valid_values]
        valid_value = pick_valid_value(valid_values, weights)
    else:
        valid_value = pick_valid_value(valid_values)
    
    # Check if this field is the error target
    if error_target == "ISA01":
        return apply_field_error("ISA01", field_spec, valid_value, error_info)
    
    return valid_value

def generate_authorization_info():
    """Generate ISA02 - Authorization Information (10 spaces)"""
    return "          "

def generate_security_qualifier(error_target=None, error_info=None):
    """Generate ISA03 - Security Information Qualifier"""
    # Generate valid value first
    field_specs = load_field_specs()
    field_spec = field_specs["ISA"]["fields"]["ISA03"]
    valid_values = field_spec.get("valid_values", [])
    # "00" most common security qualifier
    if "00" in valid_values:
        weights = [MOST_COMMON_WEIGHT if val == "00" else LESS_COMMON_WEIGHT for val in valid_values]
        valid_value = pick_valid_value(valid_values, weights)
    else:
        valid_value = pick_valid_value(valid_values)
    
    # Check if this field is the error target
    if error_target == "ISA03":
        return apply_field_error("ISA03", field_spec, valid_value, error_info)
    
    return valid_value

def generate_security_info():
    """Generate ISA04 - Security Information (10 spaces)"""
    return "          "

def generate_sender_qualifier(error_target=None, error_info=None):
    """Generate ISA05 - Interchange ID Qualifier (Sender)"""
    # Generate valid value first
    field_specs = load_field_specs()
    field_spec = field_specs["ISA"]["fields"]["ISA05"]
    valid_values = field_spec.get("valid_values", [])
    # "ZZ" most common sender qualifier 
    if "ZZ" in valid_values:
        weights = [MOST_COMMON_WEIGHT if val == "ZZ" else LESS_COMMON_WEIGHT for val in valid_values]
        valid_value = pick_valid_value(valid_values, weights)
    else:
        valid_value = pick_valid_value(valid_values)
    
    # Check if this field is the error target
    if error_target == "ISA05":
        return apply_field_error("ISA05", field_spec, valid_value, error_info)
    
    return valid_value

def generate_sender_id(error_target=None, error_info=None):
    """Generate ISA06 - Interchange Sender ID"""
    # Generate valid value first
    valid_value = random_faker_generator("company_name", 15, 15)
    
    # Check if this field is the error target
    if error_target == "ISA06":
        field_specs = load_field_specs()
        field_spec = field_specs["ISA"]["fields"]["ISA06"]
        return apply_field_error("ISA06", field_spec, valid_value, error_info)
    
    return valid_value

def generate_receiver_qualifier(error_target=None, error_info=None):
    """Generate ISA07 - Interchange ID Qualifier (Receiver)"""
    # Generate valid value first
    field_specs = load_field_specs()
    field_spec = field_specs["ISA"]["fields"]["ISA07"]
    valid_values = field_spec.get("valid_values", [])
    # "ZZ" most common receiver qualifier
    if "ZZ" in valid_values:
        weights = [MOST_COMMON_WEIGHT if val == "ZZ" else LESS_COMMON_WEIGHT for val in valid_values]
        valid_value = pick_valid_value(valid_values, weights)
    else:
        valid_value = pick_valid_value(valid_values)
    
    # Check if this field is the error target
    if error_target == "ISA07":
        return apply_field_error("ISA07", field_spec, valid_value, error_info)
    
    return valid_value

def generate_receiver_id(error_target=None, error_info=None):
    """Generate ISA08 - Interchange Receiver ID"""
    # Generate valid value first
    valid_value = random_faker_generator("insurance_provider", 15, 15)
    
    # Check if this field is the error target
    if error_target == "ISA08":
        field_specs = load_field_specs()
        field_spec = field_specs["ISA"]["fields"]["ISA08"]
        return apply_field_error("ISA08", field_spec, valid_value, error_info)
    
    return valid_value

def generate_interchange_date(error_target=None, error_info=None):
    """Generate ISA09 - Interchange Date"""
    # Generate valid value first
    valid_value = random_past_date_generator("YYMMDD", days_back=365*30)
    
    # Check if this field is the error target
    if error_target == "ISA09":
        field_specs = load_field_specs()
        field_spec = field_specs["ISA"]["fields"]["ISA09"]
        return apply_field_error("ISA09", field_spec, valid_value, error_info)
    
    return valid_value

def generate_interchange_time(error_target=None, error_info=None):
    """Generate ISA10 - Interchange Time"""
    # Generate valid value first
    valid_value = random_time_generator("HHMM")
    
    # Check if this field is the error target
    if error_target == "ISA10":
        field_specs = load_field_specs()
        field_spec = field_specs["ISA"]["fields"]["ISA10"]
        return apply_field_error("ISA10", field_spec, valid_value, error_info)
    
    return valid_value

def generate_repetition_separator(error_target=None, error_info=None):
    """Generate ISA11 - Repetition Separator"""
    # Generate valid value first
    field_specs = load_field_specs()
    field_spec = field_specs["ISA"]["fields"]["ISA11"]
    valid_values = field_spec.get("valid_values", [])
    # "^" most common repetition separator
    if "^" in valid_values:
        weights = [MOST_COMMON_WEIGHT if val == "^" else LESS_COMMON_WEIGHT for val in valid_values]
        valid_value = pick_valid_value(valid_values, weights)
    else:
        valid_value = pick_valid_value(valid_values)
    
    # Check if this field is the error target
    if error_target == "ISA11":
        return apply_field_error("ISA11", field_spec, valid_value, error_info)
    
    return valid_value

def generate_version_number(error_target=None, error_info=None):
    """Generate ISA12 - Interchange Version Number"""
    # Generate valid value first
    field_specs = load_field_specs()
    field_spec = field_specs["ISA"]["fields"]["ISA12"]
    valid_values = field_spec.get("valid_values", [])
    # "00501" most common version number
    if "00501" in valid_values:
        weights = [MOST_COMMON_WEIGHT if val == "00501" else LESS_COMMON_WEIGHT for val in valid_values]
        valid_value = pick_valid_value(valid_values, weights)
    else:
        valid_value = pick_valid_value(valid_values)
    
    # Check if this field is the error target
    if error_target == "ISA12":
        return apply_field_error("ISA12", field_spec, valid_value, error_info)
    
    return valid_value

def generate_acknowledgment_requested(error_target=None, error_info=None):
    """Generate ISA14 - Acknowledgment Requested"""
    # Generate valid value first
    field_specs = load_field_specs()
    field_spec = field_specs["ISA"]["fields"]["ISA14"]
    valid_values = field_spec.get("valid_values", [])
    # "0" most common acknowledgment request
    if "0" in valid_values:
        weights = [0.9 if val == "0" else 0.1 for val in valid_values]
        valid_value = pick_valid_value(valid_values, weights)
    else:
        valid_value = pick_valid_value(valid_values)
    
    # Check if this field is the error target
    if error_target == "ISA14":
        return apply_field_error("ISA14", field_spec, valid_value, error_info)
    
    return valid_value

def generate_usage_indicator(error_target=None, error_info=None):
    """Generate ISA15 - Usage Indicator"""
    # Generate valid value first
    field_specs = load_field_specs()
    field_spec = field_specs["ISA"]["fields"]["ISA15"]
    valid_values = field_spec.get("valid_values", [])
    # "P" is most common usage indicator but we prefer "T" for safety
    if "T" in valid_values:
        weights = [0.9 if val == "T" else 0.1 for val in valid_values]
        valid_value = pick_valid_value(valid_values, weights)
    else:
        valid_value = pick_valid_value(valid_values)
    
    # Check if this field is the error target
    if error_target == "ISA15":
        return apply_field_error("ISA15", field_spec, valid_value, error_info)
    
    return valid_value

def generate_component_separator(error_target=None, error_info=None):
    """Generate ISA16 - Component Element Separator"""
    # Generate valid value first
    field_specs = load_field_specs()
    field_spec = field_specs["ISA"]["fields"]["ISA16"]
    valid_values = field_spec.get("valid_values", [])
    # ":" most common component separator
    if ":" in valid_values:
        weights = [MOST_COMMON_WEIGHT if val == ":" else LESS_COMMON_WEIGHT for val in valid_values]
        valid_value = pick_valid_value(valid_values, weights)
    else:
        valid_value = pick_valid_value(valid_values)
    
    # Check if this field is the error target
    if error_target == "ISA16":
        return apply_field_error("ISA16", field_spec, valid_value, error_info)
    
    return valid_value

# Shared Field Generator
def generate_control_number():
    """Generate shared control number for ISA13/IEA02"""
    # Most control numbers are small numbers with leading zeros 
    if random.random() < 0.7:
        # Generate 1-6 significant digits, pad with leading zeros
        significant_digits = random.randint(1, 6)
        max_value = 10 ** significant_digits - 1
        number = random.randint(1, max_value)
        return f"{number:09d}"  # Pad to 9 digits with leading zeros
    else:
        # Generate full 9-digit control number which is less common in the wild
        return random_string_generator("numeric", 9, 9)

# ISA Segment Generator
def generate_isa_segment(with_errors=False, error_info=None, control_number=None):
    """Generate ISA segment - Interchange Control Header"""
    # Generate all valid values first
    if control_number is None:
        control_number = generate_control_number()
    
    # Determine which field should have error (if any)
    error_target = error_info.get("error_field") if error_info and error_info.get("error_target") == "FIELD" else None
    
    field_values = [
        generate_authorization_qualifier(error_target, error_info),        # ISA01
        generate_authorization_info(),                                     # ISA02
        generate_security_qualifier(error_target, error_info),             # ISA03
        generate_security_info(),                                          # ISA04
        generate_sender_qualifier(error_target, error_info),               # ISA05
        generate_sender_id(error_target, error_info),                      # ISA06
        generate_receiver_qualifier(error_target, error_info),             # ISA07
        generate_receiver_id(error_target, error_info),                    # ISA08
        generate_interchange_date(error_target, error_info),               # ISA09
        generate_interchange_time(error_target, error_info),               # ISA10
        generate_repetition_separator(error_target, error_info),           # ISA11
        generate_version_number(error_target, error_info),                 # ISA12
        control_number,                                                    # ISA13
        generate_acknowledgment_requested(error_target, error_info),       # ISA14
        generate_usage_indicator(error_target, error_info),                # ISA15
        generate_component_separator(error_target, error_info)             # ISA16
    ]
    
    # Build ISA segment string
    isa_segment = f"ISA*{'*'.join(field_values)}~"
    
    # Handle structural errors if this segment is the target
    if error_info and error_info.get("error_target") == "SEGMENT" and error_info.get("error_segment") == "ISA":
        from .error_generator import structural_error_generator
        structural_error_generator("isa_structural_error", field_values, error_info)
        
        # Return the modified segment (empty string for missing segment)
        return error_info["error_value"]
    
    return isa_segment

#=============================================================================
# IEA SEGMENT
#=============================================================================

# IEA Field Generators
def generate_group_count(error_target=None, error_info=None):
    """Generate IEA01 - Number of Functional Groups"""
    # Generate valid value first
    valid_value = "1"
    
    # Check if this field is the error target
    if error_target == "IEA01":
        field_specs = load_field_specs()
        field_spec = field_specs["IEA"]["fields"]["IEA01"]
        return apply_field_error("IEA01", field_spec, valid_value, error_info)
    
    return valid_value

def generate_iea_control_number(control_number, error_target=None, error_info=None):
    """Generate IEA02 - Interchange Control Number"""
    # Generate valid value first (use provided control number)
    valid_value = control_number
    
    # Check if this field is the error target
    if error_target == "IEA02":
        field_specs = load_field_specs()
        field_spec = field_specs["IEA"]["fields"]["IEA02"]
        return apply_field_error("IEA02", field_spec, valid_value, error_info)
    
    return valid_value

# IEA Segment Generator
def generate_iea_segment(with_errors=False, error_info=None, control_number=None):
    """Generate IEA segment - Interchange Control Trailer"""
    # Generate all valid values first
    if control_number is None:
        control_number = generate_control_number()
    
    # Determine which field should have error (if any)
    error_target = error_info.get("error_field") if error_info and error_info.get("error_target") == "FIELD" else None
    
    field_values = [
        generate_group_count(error_target, error_info),            # IEA01
        generate_iea_control_number(control_number, error_target, error_info)  # IEA02
    ]
    
    # Build IEA segment string
    iea_segment = f"IEA*{'*'.join(field_values)}~"
    
    # Handle structural errors if this segment is the target
    if error_info and error_info.get("error_target") == "SEGMENT" and error_info.get("error_segment") == "IEA":
        from .error_generator import structural_error_generator
        structural_error_generator("iea_structural_error", field_values, error_info)
        
        # Return the modified segment (empty string for missing segment)
        return error_info["error_value"]
    
    return iea_segment

#=============================================================================
# OTHER SEGMENTS (STUBBED)
#=============================================================================

def generate_gs_segment(error_info=None):
    """Generate GS segment - Functional Group Header"""
    return "GS*BE*SENDER*RECEIVER*20250915*1010*1*X*005010X220A1~"

def generate_ge_segment(error_info=None):
    """Generate GE segment - Functional Group Trailer"""
    return "GE*1*1~"

def generate_st_segment(error_info=None):
    """Generate ST segment - Transaction Set Header"""
    return "ST*834*0001*005010X220A1~"

def generate_se_segment(error_info=None):
    """Generate SE segment - Transaction Set Trailer"""
    return "SE*13*0001~"

# BGN segment moved to header_segment_generator.py

def generate_envelope_data(error_info=None):
    """Generate envelope data"""
    # Generate control number once for ISA/IEA pair
    control_number = generate_control_number()
    
    return {
        "isa": [generate_isa_segment(with_errors=False, error_info=error_info, control_number=control_number)],
        "gs": [generate_gs_segment(error_info)],
        "st": [generate_st_segment(error_info)],
        "se": [generate_se_segment(error_info)],
        "ge": [generate_ge_segment(error_info)],
        "iea": [generate_iea_segment(with_errors=False, error_info=error_info, control_number=control_number)]
        # BGN moved to header_segment_generator.py
    }

"""

TODO:
 - Implement date/time error injection for ISA09 (date) and ISA10 (time)
 - Implement structural error injection for ISA/IEA segments
 - Implement realistic auth/security info generation:
   * If ISA01="01" (password), ISA02 should contain random password string (not blank)
   * If ISA01="02" (shared secret), ISA02 should contain random secret string (not blank)
   * If ISA03="01" (password), ISA04 should contain random password string (not blank)
   * If ISA03="02" (shared secret), ISA04 should contain random secret string (not blank)
 - Implement complete segment generators (valid fields + error injection) for:
   * GS (Functional Group Header) - 8 fields - currently returns hardcoded string
   * GE (Functional Group Trailer) - 2 fields - currently returns hardcoded string
   * ST (Transaction Set Header) - 3 fields - currently returns hardcoded string
   * SE (Transaction Set Trailer) - 2 fields - currently returns hardcoded string
   * BGN moved to header_segment_generator.py
- Add production vs training mode toggle for date ranges (30 years vs 3 years)
 - Create error_rate.yaml from real production data to replace hardcoded field weights


"""


