"""
Coverage Segment Generator

Generates coverage-related segments and their field generators for EDI 834 transactions.
Handles policy/benefits information segments: N1, INS, REF, DTP, HD, COB.
"""

from .error_generator import field_error_generator, structural_error_generator
import random


def generate_n1_segment(error_info=None):
    """Generate N1 segment - Name"""
    return "N1*P5*ACME CORPORATION*FI*123456789~"


def generate_ins_segment(error_info=None):
    """Generate INS segment - Insured Benefit"""
    return "INS*Y*18*001***FT~"


def generate_ref_segment(error_info=None):
    """Generate REF segment - Reference Information"""
    return "REF*0F*987654321~"


def generate_dtp_segment(error_info=None):
    """Generate DTP segment - Date or Time Period"""
    return "DTP*356*D8*20250917~"


def generate_hd_segment(error_info=None):
    """Generate HD segment - Health Coverage"""
    return "HD*021**HLT*PLAN001~"


def generate_cob_segment(error_info=None):
    """Generate COB segment - Coordination of Benefits"""
    return "COB*P*890111*5~"


# Field generators for coverage segments
def generate_n1_entity_identifier_code(error_info=None):
    """Generate N101 field - Entity Identifier Code"""
    return "P5"


def generate_n1_name(error_info=None):
    """Generate N102 field - Name"""
    return "ACME CORPORATION"


def generate_ins_yes_no_condition_or_response_code(error_info=None):
    """Generate INS01 field - Yes/No Condition or Response Code"""
    return "Y"


def generate_ins_individual_relationship_code(error_info=None):
    """Generate INS02 field - Individual Relationship Code"""
    return "18"


def generate_ins_maintenance_type_code(error_info=None):
    """Generate INS03 field - Maintenance Type Code"""
    return "001"


def generate_ref_reference_identification_qualifier(error_info=None):
    """Generate REF01 field - Reference Identification Qualifier"""
    return "0F"


def generate_ref_reference_identification(error_info=None):
    """Generate REF02 field - Reference Identification"""
    return "987654321"


def generate_dtp_date_time_qualifier(error_info=None):
    """Generate DTP01 field - Date Time Qualifier"""
    return "356"


def generate_dtp_date_time_period_format_qualifier(error_info=None):
    """Generate DTP02 field - Date Time Period Format Qualifier"""
    return "D8"


def generate_dtp_date_time_period(error_info=None):
    """Generate DTP03 field - Date Time Period"""
    return "20250917"


def generate_hd_maintenance_type_code(error_info=None):
    """Generate HD01 field - Maintenance Type Code"""
    return "021"


def generate_hd_insurance_line_code(error_info=None):
    """Generate HD03 field - Insurance Line Code"""
    return "HLT"


def generate_hd_plan_coverage_description(error_info=None):
    """Generate HD04 field - Plan Coverage Description"""
    return "PLAN001"


def generate_cob_payer_responsibility_sequence_number_code(error_info=None):
    """Generate COB01 field - Payer Responsibility Sequence Number Code"""
    return "P"


def generate_cob_reference_identification(error_info=None):
    """Generate COB02 field - Reference Identification"""
    return "890111"


def generate_cob_coordination_of_benefits_code(error_info=None):
    """Generate COB03 field - Coordination of Benefits Code"""
    return "5"
