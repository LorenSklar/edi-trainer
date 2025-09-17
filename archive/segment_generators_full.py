"""
EDI 834 Segment Generators

Pure functions for generating individual EDI segments using faker data.
Each function returns either clean data or data with realistic errors.
"""

from faker import Faker
import random
from typing import Dict, List, Optional
from .error_generators import generate_wrong_field, get_error_explanation

fake = Faker()


def generate_isa_segment(with_errors: bool = False) -> str:
    """Generate ISA (Interchange Control Header) segment"""
    if with_errors:
        # Use systematic error generation
        sender_id = generate_wrong_field("id", "SENDER", random.choice(["missing", "wrong_length", "wrong_format"]))
        receiver_id = generate_wrong_field("id", "RECEIVER", random.choice(["missing", "wrong_length", "wrong_format"]))
        date = generate_wrong_field("date", "250917", random.choice(["wrong_format", "wrong_length"]))
        time = generate_wrong_field("time", "1430", random.choice(["wrong_format", "wrong_length"]))
        control_num = generate_wrong_field("control_number", "000000001", random.choice(["missing", "wrong_length"]))
    else:
        sender_id = fake.random_element(elements=("SENDER", "COMPANY", "HR_SYS"))
        receiver_id = fake.random_element(elements=("RECEIVER", "CARRIER", "BCBS"))
        date = fake.date(pattern="%y%m%d")  # Correct YYMMDD format
        time = fake.time(pattern="%H%M")
        control_num = fake.random_number(digits=9)
    
    return f"ISA*00*          *00*          *ZZ*{sender_id:<15}*ZZ*{receiver_id:<15}*{date}*{time}*^*00501*{control_num}*0*P*:~"


def generate_gs_segment(with_errors: bool = False) -> str:
    """Generate GS (Functional Group Header) segment"""
    if with_errors:
        # Common GS errors: wrong functional identifier, wrong version
        func_id = fake.random_element(elements=("HC", "HP", "FA"))  # Wrong functional IDs
        version = fake.random_element(elements=("004010X096A1", "003010X096A1", "005010X220A10", "005010X330A1", "005010X220B3"))  # Wrong versions
    else:
        func_id = "BE"  # Benefits Enrollment
        version = "005010X220A1"  # Correct 834 version
    
    sender_gs = fake.random_element(elements=("SENDERGS", "COMPANYGS", "HR_GS"))
    receiver_gs = fake.random_element(elements=("RECEIVERGS", "CARRIERGS", "BCBS_GS"))
    date = fake.date(pattern="%Y%m%d")
    time = fake.time(pattern="%H%M")
    control_num = fake.random_number(digits=9)
    
    return f"GS*{func_id}*{sender_gs}*{receiver_gs}*{date}*{time}*{control_num}*X*{version}~"


def generate_st_segment(with_errors: bool = False) -> str:
    """Generate ST (Transaction Set Header) segment"""
    if with_errors:
        # Common ST errors: wrong transaction set ID, completely wrong version
        trans_id = fake.random_element(elements=("835", "837", "820"))  # Wrong transaction types
        version = fake.random_element(elements=("004010X096A1", "003010X096A1", "005010X222A1"))  # Completely wrong versions
    else:
        trans_id = "834"  # Health Care Benefit Enrollment
        version = "005010X220A1"  # Correct 834 version
    
    control_num = fake.random_number(digits=4)
    return f"ST*{trans_id}*{control_num}*{version}~"


def generate_bgn_segment(with_errors: bool = False) -> str:
    """Generate BGN (Beginning Segment) segment"""
    if with_errors:
        # Common BGN errors: missing purpose code, wrong date format
        purpose = fake.random_element(elements=("", "01", "02"))  # Missing or wrong purpose codes
        date = fake.date(pattern="%m/%d/%Y")  # Wrong format
    else:
        purpose = "00"  # Original
        date = fake.date(pattern="%Y%m%d")  # Correct format
    
    ref_id = fake.random_number(digits=5)
    time = fake.time(pattern="%H%M%S")
    
    return f"BGN*{purpose}*{ref_id}*{date}*{time}****4~"


def generate_n1_segment(with_errors: bool = False) -> str:
    """Generate N1 (Name) segment for Payor"""
    if with_errors:
        # Common N1 errors: missing entity identifier, invalid qualifier
        entity_id = fake.random_element(elements=("", "P1", "P2"))  # Missing or wrong entity IDs
        qualifier = fake.random_element(elements=("", "NI", "PI"))  # Missing or wrong qualifiers
    else:
        entity_id = "P5"  # Payor
        qualifier = "FI"  # Federal Taxpayer's Identification Number
    
    company_name = fake.company()
    tax_id = fake.random_number(digits=9)
    
    return f"N1*{entity_id}*{company_name}*{qualifier}*{tax_id}~"


def generate_ins_segment(with_errors: bool = False) -> str:
    """Generate INS (Insured) segment"""
    if with_errors:
        # Common INS errors: missing maintenance type, wrong relationship code
        maint_type = fake.random_element(elements=("", "21", "22"))  # Missing or wrong maintenance types
        relationship = fake.random_element(elements=("", "003", "004"))  # Missing or wrong relationship codes
    else:
        maint_type = fake.random_element(elements=("18", "19", "20"))  # Add, Change, Delete
        relationship = fake.random_element(elements=("001", "002", "034"))  # Spouse, Child, Self
    
    yes_no = fake.random_element(elements=("Y", "N"))
    employment_status = fake.random_element(elements=("FT", "PT", "RT"))  # Full-time, Part-time, Retired
    
    return f"INS*{yes_no}*{maint_type}*{relationship}***{employment_status}~"


def generate_ref_segment(ref_type: str = "0F", with_errors: bool = False) -> str:
    """Generate REF (Reference Information) segment"""
    if with_errors:
        # Common REF errors: missing reference qualifier, malformed ID
        if ref_type == "0F":  # Member ID
            ref_id = fake.random_element(elements=("", "1234567890", "ABCDEFGHI"))  # Missing or wrong length/format
        else:  # SSN
            ref_id = fake.random_element(elements=("", "123-45-6789", "000-00-0000"))  # Missing or with dashes
    else:
        if ref_type == "0F":  # Member ID
            ref_id = fake.random_number(digits=9)
        else:  # SSN
            ref_id = fake.ssn().replace("-", "")  # Remove dashes for EDI
    
    return f"REF*{ref_type}*{ref_id}~"


def generate_dtp_segment(dtp_type: str = "356", with_errors: bool = False) -> str:
    """Generate DTP (Date/Time/Period) segment"""
    if with_errors:
        # Common DTP errors: wrong date format, invalid qualifier
        date_format = fake.random_element(elements=("D6", "D7", "D9"))  # Wrong formats
        date = fake.date(pattern="%m/%d/%Y")  # Wrong format
    else:
        date_format = "D8"  # CCYYMMDD format
        date = fake.date(pattern="%Y%m%d")  # Correct format
    
    return f"DTP*{dtp_type}*{date_format}*{date}~"


def generate_nm1_segment(with_errors: bool = False) -> str:
    """Generate NM1 (Individual Name) segment"""
    if with_errors:
        # Common NM1 errors: missing entity type, malformed SSN
        entity_type = fake.random_element(elements=("", "PR", "QC"))  # Missing or wrong entity types
        ssn = fake.random_element(elements=("", "123-45-6789", "000-00-0000"))  # Missing or with dashes
    else:
        entity_type = "IL"  # Insured
        ssn = fake.ssn().replace("-", "")  # Remove dashes
    
    name_type = "1"  # Person
    last_name = fake.last_name()
    first_name = fake.first_name()
    middle_name = fake.first_name() if fake.boolean() else ""
    name_suffix = fake.random_element(elements=("JR", "SR", "III", ""))
    id_type = "34"  # Social Security Number
    
    return f"NM1*{entity_type}*{name_type}*{last_name}*{first_name}*{middle_name}***{name_suffix}*{id_type}*{ssn}~"


def generate_dmg_segment(with_errors: bool = False) -> str:
    """Generate DMG (Demographic Information) segment"""
    if with_errors:
        # Common DMG errors: missing date format, invalid gender code
        date_format = fake.random_element(elements=("", "D6", "D7"))  # Missing or wrong formats
        birth_date = fake.date(pattern="%m/%d/%Y")  # Wrong format
        gender = fake.random_element(elements=("", "X", "Y"))  # Missing or invalid gender codes
    else:
        date_format = "D8"  # CCYYMMDD format
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%Y%m%d")
        gender = fake.random_element(elements=("M", "F"))
    
    return f"DMG*{date_format}*{birth_date}*{gender}~"


def generate_hd_segment(with_errors: bool = False) -> str:
    """Generate HD (Health Coverage) segment"""
    if with_errors:
        # Common HD errors: missing maintenance type, wrong plan type
        maint_type = fake.random_element(elements=("", "022", "026"))  # Missing or wrong maintenance types
        plan_type = fake.random_element(elements=("", "MED", "RX"))  # Missing or wrong plan types
    else:
        maint_type = fake.random_element(elements=("021", "024", "025"))  # Add, Change, Delete
        plan_type = fake.random_element(elements=("HLT", "DEN", "VIS"))  # Health, Dental, Vision
    
    plan_name = fake.random_element(elements=("PLAN001", "BASIC", "PREMIUM"))
    
    return f"HD*{maint_type}**{plan_type}*{plan_name}~"


def generate_se_segment(segment_count: int, with_errors: bool = False) -> str:
    """Generate SE (Transaction Set Trailer) segment"""
    if with_errors:
        # Common SE errors: wrong segment count
        segment_count = fake.random_element(elements=(segment_count + 1, segment_count - 1, 0))
    
    control_num = fake.random_number(digits=4)
    return f"SE*{segment_count}*{control_num}~"


def generate_ge_segment(with_errors: bool = False) -> str:
    """Generate GE (Functional Group Trailer) segment"""
    if with_errors:
        # Common GE errors: wrong transaction count
        transaction_count = fake.random_element(elements=(0, 999, -1))
    else:
        transaction_count = 1
    
    control_num = fake.random_number(digits=9)
    return f"GE*{transaction_count}*{control_num}~"


def generate_iea_segment(with_errors: bool = False) -> str:
    """Generate IEA (Interchange Control Trailer) segment"""
    if with_errors:
        # Common IEA errors: wrong group count
        group_count = fake.random_element(elements=(0, 999, -1))
    else:
        group_count = 1
    
    control_num = fake.random_number(digits=9)
    return f"IEA*{group_count}*{control_num}~"
