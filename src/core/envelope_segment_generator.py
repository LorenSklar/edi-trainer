"""
Envelope Segment Generator

Generates envelope/structural segments and their field generators for EDI 834 transactions.
Handles all structural segments: ISA, IEA, GS, GE, ST, SE, BGN.
"""

from .error_generator import field_error_generator, structural_error_generator
import random

"""
TO DO: 
 - Add error injection for each field using with_errors flag
 - Update error_info as needed
 - Update shared_data as needed
"""

def generate_isa_segment(error_info=None):
    """Generate ISA segment - Interchange Control Header"""
    return "ISA*00*          *00*          *ZZ*SENDER_ID      *ZZ*RECEIVER_ID    *250917*1430*^*00501*000000001*0*T*:~"

def generate_iea_segment(error_info=None):
    """Generate IEA segment - Interchange Control Trailer"""
    return "IEA*1*000000001~"


def generate_gs_segment(error_info=None):
    """Generate GS segment - Functional Group Header"""
    return "GS*BE*SENDER*RECEIVER*20250917*1430*1*X*005010X220A1~"


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
def generate_isa_authorization_information_qualifier(with_errors=False, error_info=None):
    """Generate ISA01 field - Authorization Information Qualifier"""
    return "00"


def generate_isa_authorization_information(error_info=None):
    """Generate ISA02 field - Authorization Information"""
    return "          "


def generate_isa_security_information_qualifier(error_info=None):
    """Generate ISA03 field - Security Information Qualifier"""
    return "00"


def generate_isa_security_information(error_info=None):
    """Generate ISA04 field - Security Information"""
    return "          "


def generate_isa_interchange_id_qualifier_sender(error_info=None):
    """Generate ISA05 field - Interchange ID Qualifier (Sender)"""
    return "ZZ"


def generate_isa_interchange_sender_id(error_info=None):
    """Generate ISA06 field - Interchange Sender ID"""
    return "SENDER_ID      "


def generate_isa_interchange_id_qualifier_receiver(error_info=None):
    """Generate ISA07 field - Interchange ID Qualifier (Receiver)"""
    return "ZZ"


def generate_isa_interchange_receiver_id(error_info=None):
    """Generate ISA08 field - Interchange Receiver ID"""
    return "RECEIVER_ID    "


def generate_isa_interchange_date(error_info=None):
    """Generate ISA09 field - Interchange Date"""
    return "250917"


def generate_isa_interchange_time(error_info=None):
    """Generate ISA10 field - Interchange Time"""
    return "1430"


def generate_isa_repetition_separator(error_info=None):
    """Generate ISA11 field - Repetition Separator"""
    return "^"


def generate_isa_interchange_control_version_number(error_info=None):
    """Generate ISA12 field - Interchange Control Version Number"""
    return "00501"


def generate_isa_interchange_control_number(error_info=None):
    """Generate ISA13 field - Interchange Control Number"""
    return "000000001"


def generate_isa_acknowledgment_requested(error_info=None):
    """Generate ISA14 field - Acknowledgment Requested"""
    return "0"


def generate_isa_usage_indicator(error_info=None):
    """Generate ISA15 field - Usage Indicator"""
    return "T"


def generate_isa_component_element_separator(error_info=None):
    """Generate ISA16 field - Component Element Separator"""
    return ":"
