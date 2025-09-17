"""
EDI 834 Segment Generators

Pure functions for generating individual EDI segments using faker data.
Each function returns either clean data or data with a single realistic error.
"""

from faker import Faker
import random
from .field_generators import (
    generate_sender_id, generate_receiver_id, generate_date, 
    generate_time, generate_control_number, generate_group_count,
    generate_segment_structure_error, get_error_explanation
)

fake = Faker()


def generate_isa_iea_pair(with_errors: bool = False) -> tuple:
    """
    Generate ISA and IEA segments as a pair with matching control numbers.
    
    Args:
        with_errors: If True, introduce a single error in one of the segments
    
    Returns:
        Tuple of (ISA_segment, IEA_segment)
    """
    # Generate valid data first
    sender_id = generate_sender_id(with_errors=False)
    receiver_id = generate_receiver_id(with_errors=False)
    date = generate_date(with_errors=False)
    time = generate_time(with_errors=False)
    control_num = generate_control_number(with_errors=False)
    group_count = generate_group_count(with_errors=False)
    
    if with_errors:
        # Randomly choose which error type: field error or structural error
        error_type = random.choices(
            ["field_error", "structural_error"],
            weights=[70, 30]  # Field errors more common than structural
        )[0]
        
        if error_type == "field_error":
            # Randomly choose which field to corrupt
            error_target = random.choice([
                "isa_sender_id", "isa_receiver_id", "isa_date", "isa_time", "isa_control",
                "iea_group_count", "iea_control", "mismatched_control"
            ])
        else:
            # Structural error
            error_target = random.choice([
                "isa_missing_delimiter", "isa_extra_delimiter", "isa_missing_terminator",
                "iea_missing_delimiter", "iea_extra_delimiter", "iea_missing_terminator"
            ])
        
        if error_target == "isa_sender_id":
            sender_id = generate_sender_id(with_errors=True)
        elif error_target == "isa_receiver_id":
            receiver_id = generate_receiver_id(with_errors=True)
        elif error_target == "isa_date":
            date = generate_date(with_errors=True)
        elif error_target == "isa_time":
            time = generate_time(with_errors=True)
        elif error_target == "isa_control":
            control_num = generate_control_number(with_errors=True)
        elif error_target == "iea_group_count":
            group_count = generate_group_count(with_errors=True)
        elif error_target == "iea_control":
            control_num = generate_control_number(with_errors=True)
        elif error_target == "mismatched_control":
            # Keep ISA control number, change IEA control number
            iea_control = generate_control_number(with_errors=False)
            while iea_control == control_num:  # Ensure they're different
                iea_control = generate_control_number(with_errors=False)
            control_num = iea_control
    
    # Build segments
    isa_segment = f"ISA*00*          *00*          *ZZ*{sender_id:<15}*ZZ*{receiver_id:<15}*{date}*{time}*^*00501*{control_num}*0*P*:~"
    iea_segment = f"IEA*{group_count}*{control_num}~"
    
    # Apply structural errors if needed
    if with_errors and error_type == "structural_error":
        if error_target.startswith("isa_"):
            structural_error_type = error_target.replace("isa_", "")
            isa_segment = generate_segment_structure_error(isa_segment, structural_error_type)
        elif error_target.startswith("iea_"):
            structural_error_type = error_target.replace("iea_", "")
            iea_segment = generate_segment_structure_error(iea_segment, structural_error_type)
    
    # Return error info for GRR explanations
    error_info = None
    if with_errors:
        error_info = {
            "error_type": error_type,
            "error_target": error_target,
            "field_name": error_target.replace("isa_", "").replace("iea_", ""),
            "segment": "ISA" if error_target.startswith("isa_") else "IEA"
        }
    
    return isa_segment, iea_segment, error_info


def generate_isa_segment(with_errors: bool = False) -> str:
    """Generate ISA (Interchange Control Header) segment"""
    isa, _ = generate_isa_iea_pair(with_errors)
    return isa


def generate_iea_segment(with_errors: bool = False) -> str:
    """Generate IEA (Interchange Control Trailer) segment"""
    _, iea = generate_isa_iea_pair(with_errors)
    return iea


def get_isa_iea_error_explanation(isa_segment: str, iea_segment: str) -> str:
    """
    Analyze ISA/IEA pair and return explanation of any errors found.
    
    Args:
        isa_segment: The ISA segment to analyze
        iea_segment: The IEA segment to analyze
    
    Returns:
        Explanation of errors found, or "No errors found" if clean
    """
    # Parse ISA fields
    isa_fields = isa_segment.split('*')
    if len(isa_fields) < 16:
        return "ISA segment is malformed - missing required fields."
    
    # Parse IEA fields  
    iea_fields = iea_segment.split('*')
    if len(iea_fields) < 3:
        return "IEA segment is malformed - missing required fields."
    
    # Check for mismatched control numbers
    isa_control = isa_fields[13]  # ISA control number
    iea_control = iea_fields[2]   # IEA control number
    
    if isa_control != iea_control:
        return f"Control number mismatch: ISA has {isa_control}, IEA has {iea_control}. These must match."
    
    # Check ISA fields
    sender_id = isa_fields[6]
    receiver_id = isa_fields[8]
    date = isa_fields[9]
    time = isa_fields[10]
    
    if not sender_id or sender_id.strip() == "":
        return get_error_explanation("Sender ID", sender_id, "alphanumeric, max 15 chars")
    
    if not receiver_id or receiver_id.strip() == "":
        return get_error_explanation("Receiver ID", receiver_id, "alphanumeric, max 15 chars")
    
    if len(date) != 6:
        return get_error_explanation("Date", date, "6 digits (YYMMDD)")
    
    if len(time) != 4:
        return get_error_explanation("Time", time, "4 digits (HHMM)")
    
    # Check IEA fields
    group_count = iea_fields[1]
    if not group_count or group_count.strip() == "":
        return get_error_explanation("Group Count", group_count, "1 digit")
    
    return "No errors found - ISA/IEA pair is valid."