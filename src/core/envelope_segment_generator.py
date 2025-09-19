"""
Envelope Segment Generator

Generates envelope/structural segments and their field generators for EDI 834 transactions.
Handles all structural segments: ISA, IEA, GS, GE, ST, SE, BGN.
"""

from .error_generator import load_field_specs, is_error_in_field, field_error_generator
from .data_generator import (
    random_string_generator, random_faker_generator, 
    random_past_date_generator, random_future_date_generator, 
    random_time_generator, pick_valid_value, generate_field_value,
    load_character_sets, convert_to_safe_characterset
)
import random

"""
COMPLETED:
 - ✅ Add error injection for each field using with_errors flag
 - ✅ Update error_info as needed

TODO:
 - Create error_rate.yaml from real production data to replace hardcoded field weights
 - Implement date/time error injection for ISA09 (date) and ISA10 (time)
 - Implement structural error injection for ISA/IEA segments
 - Implement complete segment generators (valid fields + error injection) for:
   * GS (Functional Group Header) - 8 fields - currently returns hardcoded string
   * GE (Functional Group Trailer) - 2 fields - currently returns hardcoded string
   * ST (Transaction Set Header) - 3 fields - currently returns hardcoded string
   * SE (Transaction Set Trailer) - 2 fields - currently returns hardcoded string
   * BGN (Beginning Segment) - 8 fields - currently returns hardcoded string

"""


def generate_isa_segment(with_errors=False, error_info=None, control_number=None):
    """Generate ISA segment - Interchange Control Header"""
    # Generate all valid values first
    if control_number is None:
        control_number = random_string_generator("numeric", 9, 9)
    
    field_values = [
        pick_valid_value("ISA01"),                 # ISA01 - Authorization qualifier
        "          ",                               # ISA02 - Authorization info (10 spaces)
        pick_valid_value("ISA03"),                 # ISA03 - Security qualifier
        "          ",                               # ISA04 - Security info (10 spaces)
        "ZZ",                                      # ISA05 - Sender qualifier
        generate_field_value("ISA06", 15, 15),    # ISA06 - Sender ID (uses YAML field_type)
        "ZZ",                                      # ISA07 - Receiver qualifier
        generate_field_value("ISA08", 15, 15),    # ISA08 - Receiver ID (uses YAML field_type)
        random_past_date_generator("YYMMDD", days_back=30), # ISA09
        random_time_generator("HHMM"),             # ISA10
        "^",                                       # ISA11
        "00501",                                   # ISA12
        control_number,                            # ISA13
        "0",                                       # ISA14
        "T",                                       # ISA15
        ":"                                        # ISA16
    ]
    
    # Apply error to the targeted field (if any)
    if error_info and error_info.get("error_target") == "FIELD":
        field_designation = error_info.get("error_field")
        # Get field spec from nested structure
        field_specs = load_field_specs()
        segment_name = field_designation[:3]  # e.g., "ISA01" -> "ISA"
        field_spec = {}
        if segment_name in field_specs and 'fields' in field_specs[segment_name]:
            field_spec = field_specs[segment_name]['fields'].get(field_designation, {})
        
        # Map field designations to list indices
        field_index_map = {
            "ISA01": 0, "ISA02": 1, "ISA03": 2, "ISA04": 3,
            "ISA05": 4, "ISA06": 5, "ISA07": 6, "ISA08": 7,
            "ISA09": 8, "ISA10": 9, "ISA11": 10, "ISA12": 11,
            "ISA13": 12, "ISA14": 13, "ISA15": 14, "ISA16": 15
        }
        
        field_index = field_index_map.get(field_designation)
        if field_index is not None:
            error_result = field_error_generator(field_designation, field_spec, field_values[field_index])
            field_values[field_index] = error_result["error_value"]
            
            # Update error_info with the specific error details
            error_info["error_field"] = field_designation
            error_info["error_type"] = error_result["error_type"]
            error_info["error_value"] = error_result["error_value"]
            error_info["error_explanation"] = error_result["error_explanation"]
    
    # Build ISA segment string
    isa_segment = f"ISA*{'*'.join(field_values)}~"
    
    return isa_segment

def generate_iea_segment(with_errors=False, error_info=None, control_number=None):
    """Generate IEA segment - Interchange Control Trailer"""
    # Generate all valid values first
    if control_number is None:
        control_number = generate_control_number(error_info)
    
    field_values = [
        generate_group_count(error_info),  # IEA01
        control_number                     # IEA02
    ]
    
    # Apply error to the targeted field (if any)
    if error_info and error_info.get("error_target") == "FIELD":
        field_designation = error_info.get("error_field")
        # Get field spec from nested structure
        field_specs = load_field_specs()
        segment_name = field_designation[:3]  # e.g., "IEA01" -> "IEA"
        field_spec = {}
        if segment_name in field_specs and 'fields' in field_specs[segment_name]:
            field_spec = field_specs[segment_name]['fields'].get(field_designation, {})
        
        # Map field designations to list indices
        field_index_map = {
            "IEA01": 0, "IEA02": 1
        }
        
        field_index = field_index_map.get(field_designation)
        if field_index is not None:
            error_result = field_error_generator(field_designation, field_spec, field_values[field_index])
            field_values[field_index] = error_result["error_value"]
            
            # Update error_info with the specific error details
            error_info["error_field"] = field_designation
            error_info["error_type"] = error_result["error_type"]
            error_info["error_value"] = error_result["error_value"]
            error_info["error_explanation"] = error_result["error_explanation"]
    
    # Build IEA segment string
    iea_segment = f"IEA*{'*'.join(field_values)}~"
    
    return iea_segment


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


def generate_bgn_segment(error_info=None):
    """Generate BGN segment - Beginning Segment"""
    return "BGN*00*12345*20250917*143000****4~"


def generate_envelope_data(error_info=None):
    """Generate envelope data"""
    # Generate control number once for ISA/IEA pair
    control_number = generate_control_number()
    
    return {
        "isa": [generate_isa_segment(with_errors=False, error_info=error_info, control_number=control_number)],
        "gs": [generate_gs_segment(error_info)],
        "st": [generate_st_segment(error_info)],
        "bgn": [generate_bgn_segment(error_info)],
        "se": [generate_se_segment(error_info)],
        "ge": [generate_ge_segment(error_info)],
        "iea": [generate_iea_segment(with_errors=False, error_info=error_info, control_number=control_number)]
    }


# Field generators for envelope segments
def generate_authorization_qualifier(error_info=None):
    """Generate Authorization Information Qualifier field"""
    valid_value = random_string_generator("numeric", 2, 2)
    error_in_field = is_error_in_field("ISA01", error_info)
    if error_in_field:
        field_spec = load_field_specs().get("ISA01", {})
        error_result = field_error_generator("ISA01", field_spec, valid_value)
        return error_result["error_value"]
    return valid_value

def generate_authorization_information(error_info=None):
    """Generate Authorization Information field"""
    return "          "

def generate_security_qualifier(error_info=None):
    """Generate Security Information Qualifier field"""
    return "00"

def generate_security_information(error_info=None):
    """Generate Security Information field"""
    return "          "

def generate_id_qualifier_sender(error_info=None):
    """Generate ID Qualifier (Sender) field"""
    return "ZZ"

def generate_sender_id(error_info=None):
    """Generate Sender ID field"""
    return random_faker_generator("company", 15, 15)

def generate_id_qualifier_receiver(error_info=None):
    """Generate ID Qualifier (Receiver) field"""
    return "ZZ"

def generate_receiver_id(error_info=None):
    """Generate Receiver ID field"""
    return random_faker_generator("company", 15, 15)

def generate_interchange_date(error_info=None):
    """Generate Interchange Date field"""
    return random_past_date_generator("YYMMDD", days_back=30)

def generate_interchange_time(error_info=None):
    """Generate Interchange Time field"""
    return random_time_generator("HHMM")

def generate_repetition_separator(error_info=None):
    """Generate Repetition Separator field"""
    return "^"

def generate_version_number(error_info=None):
    """Generate Control Version Number field"""
    return "00501"

def generate_control_number(error_info=None):
    """Generate Control Number field"""
    return random_string_generator("numeric", 9, 9)

def generate_acknowledgment_requested(error_info=None):
    """Generate Acknowledgment Requested field"""
    return "0"

def generate_usage_indicator(error_info=None):
    """Generate Usage Indicator field"""
    return "T"

def generate_component_separator(error_info=None):
    """Generate Component Element Separator field"""
    return ":"

def generate_group_count(error_info=None):
    """Generate Number of Functional Groups field"""
    return "1"

