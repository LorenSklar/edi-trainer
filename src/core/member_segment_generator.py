"""
Member Segment Generator

Generates member-related segments and their field generators for EDI 834 transactions.
Handles personal/demographic information segments: NM1, PER, N3, N4, DMG.
"""

from .error_generator import field_error_generator, structural_error_generator
import random


def generate_nm1_segment(error_info=None):
    """Generate NM1 segment - Individual or Organizational Name"""
    return "NM1*IL*1*DOE*JOHN*M***34*987654321~"


def generate_per_segment(error_info=None):
    """Generate PER segment - Member Communications Numbers"""
    return "PER*IP**HP*7172343334*WP*7172341240~"


def generate_n3_segment(error_info=None):
    """Generate N3 segment - Address Information"""
    return "N3*100 MARKET ST*APT 3G~"


def generate_n4_segment(error_info=None):
    """Generate N4 segment - Geographic Location"""
    return "N4*CAMP HILL*PA*17011**CY*CUMBERLAND~"


def generate_dmg_segment(error_info=None):
    """Generate DMG segment - Demographic Information"""
    return "DMG*D8*19900115*M~"


# Field generators for member segments
def generate_nm1_entity_identifier_code(error_info=None):
    """Generate NM101 field - Entity Identifier Code"""
    return "IL"


def generate_nm1_entity_type_qualifier(error_info=None):
    """Generate NM102 field - Entity Type Qualifier"""
    return "1"


def generate_nm1_name_last(error_info=None):
    """Generate NM103 field - Name Last or Organization Name"""
    return "DOE"


def generate_nm1_name_first(error_info=None):
    """Generate NM104 field - Name First"""
    return "JOHN"


def generate_nm1_name_middle(error_info=None):
    """Generate NM105 field - Name Middle"""
    return "M"


def generate_dmg_date_time_period_format_qualifier(error_info=None):
    """Generate DMG01 field - Date Time Period Format Qualifier"""
    return "D8"


def generate_dmg_date_time_period(error_info=None):
    """Generate DMG02 field - Date Time Period"""
    return "19900115"


def generate_dmg_gender_code(error_info=None):
    """Generate DMG03 field - Gender Code"""
    return "M"
