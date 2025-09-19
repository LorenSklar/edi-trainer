"""
Envelope Segment Generator

Generates envelope/structural segments and their field generators for EDI 834 transactions.
Handles all structural segments: ISA, IEA, GS, GE, ST, SE, BGN.
"""

from .error_generator import load_field_specs
import random

"""
TO DO: 
 - Add error injection for each field using with_errors flag
 - Update error_info as needed
 - Create error_rate.yaml from real production data to replace hardcoded field weights
"""

def generate_isa_segment(error_info=None, control_number=None):
    """Generate ISA segment - Interchange Control Header"""
    # Load field specifications
    field_specs = load_field_specs()
    isa_fields = {}
    
    # Generate ISA fields using individual field generators
    authorization_qualifier = generate_authorization_qualifier(error_info)
    authorization_information = generate_authorization_information(error_info)
    security_qualifier = generate_security_qualifier(error_info)
    security_information = generate_security_information(error_info)
    id_qualifier_sender = generate_id_qualifier_sender(error_info)
    sender_id = generate_sender_id(error_info)
    id_qualifier_receiver = generate_id_qualifier_receiver(error_info)
    receiver_id = generate_receiver_id(error_info)
    interchange_date = generate_interchange_date(error_info)
    interchange_time = generate_interchange_time(error_info)
    repetition_separator = generate_repetition_separator(error_info)
    version_number = generate_control_version_number(error_info)
    if control_number is None:
        control_number = generate_control_number(error_info)
    acknowledgment_requested = generate_acknowledgment_requested(error_info)
    usage_indicator = generate_usage_indicator(error_info)
    component_separator = generate_component_separator(error_info)
    
    # Build ISA segment string
    isa_segment = f"ISA*{authorization_qualifier}*{authorization_information}*{security_qualifier}*{security_information}*{id_qualifier_sender}*{sender_id}*{id_qualifier_receiver}*{receiver_id}*{interchange_date}*{interchange_time}*{repetition_separator}*{version_number}*{control_number}*{acknowledgment_requested}*{usage_indicator}*{component_separator}~"
    
    return isa_segment

def generate_iea_segment(error_info=None, control_number=None):
    """Generate IEA segment - Interchange Control Trailer"""
    # Generate IEA fields using individual field generators
    group_count = generate_group_count(error_info)
    if control_number is None:
        control_number = generate_control_number(error_info)
    
    # Build IEA segment string
    iea_segment = f"IEA*{group_count}*{control_number}~"
    
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


# Field generators for envelope segments
def generate_authorization_qualifier(with_errors=False, error_info=None):
    """Generate Authorization Information Qualifier field"""
    return "00"


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
    return "SENDER_ID      "


def generate_id_qualifier_receiver(error_info=None):
    """Generate ID Qualifier (Receiver) field"""
    return "ZZ"


def generate_receiver_id(error_info=None):
    """Generate Receiver ID field"""
    return "RECEIVER_ID    "


def generate_interchange_date(error_info=None):
    """Generate Interchange Date field"""
    return "250917"


def generate_interchange_time(error_info=None):
    """Generate Interchange Time field"""
    return "1430"


def generate_repetition_separator(error_info=None):
    """Generate Repetition Separator field"""
    return "^"


def generate_control_version_number(error_info=None):
    """Generate Control Version Number field"""
    return "00501"


def generate_control_number(error_info=None):
    """Generate Control Number field"""
    return "000000001"


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






def generate_envelope_data(error_info=None):
    """Generate envelope data"""
    # Generate control number once for ISA/IEA pair
    control_number = generate_control_number(error_info)
    
    return {
        "isa": [generate_isa_segment(error_info, control_number)],
        "gs": [generate_gs_segment(error_info)],
        "st": [generate_st_segment(error_info)],
        "bgn": [generate_bgn_segment(error_info)],
        "se": [generate_se_segment(error_info)],
        "ge": [generate_ge_segment(error_info)],
        "iea": [generate_iea_segment(error_info, control_number)]
    }
