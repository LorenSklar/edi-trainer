"""
EDI 834 Segment Generators

Pure functions for generating individual EDI segments using faker data.
Each function returns either clean data or data with a single realistic error.
"""

from faker import Faker
import random
from .field_generators import (
    generate_acknowledgment_code, generate_control_number, generate_date,
    generate_group_count, generate_receiver_id, generate_receiver_qualifier,
    generate_sender_id, generate_sender_qualifier, generate_segment_structure_error,
    generate_time, generate_usage_indicator, generate_version, get_error_explanation
)

fake = Faker()


def generate_isa_iea_pair(with_errors: bool = False) -> dict:
    """
    Generate ISA and IEA segments as a pair with matching control numbers.
    
    Args:
        with_errors: If True, introduce a single error in one of the segments
    
    Returns:
        Dictionary containing:
        - isa_segment: ISA segment string
        - iea_segment: IEA segment string  
        - error_info: Error details or None if no errors
        - shared_data: Dictionary of shared field values for consistency across segments
    """
    # Generate valid data first
    sender_qualifier = generate_sender_qualifier(with_errors=False)
    sender_id = generate_sender_id(with_errors=False)
    receiver_qualifier = generate_receiver_qualifier(with_errors=False)
    receiver_id = generate_receiver_id(with_errors=False)
    date = generate_date(with_errors=False)
    time = generate_time(with_errors=False)
    version = generate_version(with_errors=False)
    acknowledgment_code = generate_acknowledgment_code(with_errors=False)
    control_number = generate_control_number(with_errors=False)
    usage_indicator = generate_usage_indicator(with_errors=False)
    group_count = generate_group_count(with_errors=False)
    
    if with_errors:
        # Choose random error type -- field error or structural error -- with realistic weights
        error_type = random.choices(
            ["field_error", "structural_error"],
            weights=[70, 30] 
        )[0]
        
        if error_type == "field_error":
            # Choose random field to corrupt with equal weights
            error_target = random.choice([
                "sender_qualifier", "sender_id", "receiver_qualifier", "receiver_id", 
                "date", "time", "version", "acknowledgment_code", "control_number", "usage_indicator",
                "group_count"
            ])
        else:
            # Structural error with realistic weights
            error_target = random.choices([
                "missing_entire_envelope", 
                "isa_missing_delimiter", "isa_extra_delimiter", "isa_missing_terminator",
                "isa_missing_field", "isa_blank_field",
                "iea_missing_delimiter", "iea_extra_delimiter", "iea_missing_terminator", 
                "iea_missing_field", "iea_blank_field",
                "mismatched_control", "incorrect_group_count"
            ], weights=[
                50,
                10, 10, 5,  # isa delimiter/terminator errors
                5, 5,  # isa field errors
                10, 10, 5,  # iea delimiter/terminator errors  
                5, 5,  # iea field errors
                5, 5  # structural relationship errors
            ])[0]
        
        if error_target == "sender_qualifier":
            sender_qualifier = generate_sender_qualifier(with_errors=True)
        elif error_target == "sender_id":
            sender_id = generate_sender_id(with_errors=True)
        elif error_target == "receiver_qualifier":
            receiver_qualifier = generate_receiver_qualifier(with_errors=True)
        elif error_target == "receiver_id":
            receiver_id = generate_receiver_id(with_errors=True)
        elif error_target == "date":
            date = generate_date(with_errors=True)
        elif error_target == "time":
            time = generate_time(with_errors=True)
        elif error_target == "version":
            version = generate_version(with_errors=True)
        elif error_target == "acknowledgment_code":
            acknowledgment_code = generate_acknowledgment_code(with_errors=True)
        elif error_target == "usage_indicator":
            usage_indicator = generate_usage_indicator(with_errors=True)
        elif error_target == "control_number":
            control_number = generate_control_number(with_errors=True)
        elif error_target == "group_count":
            group_count = generate_group_count(with_errors=True)
    
    # Build segments
    isa_segment = f"ISA*00*          *00*          *{sender_qualifier}*{sender_id}*{receiver_qualifier}*{receiver_id}*{date}*{time}*^*{version}*{control_number}*{acknowledgment_code}*{usage_indicator}*:~"
    iea_segment = f"IEA*{group_count}*{control_number}~"
    
    # Apply structural errors if needed
    if with_errors and error_type == "structural_error":
        if error_target == "missing_entire_envelope":
            # Return empty segments to simulate missing envelope
            isa_segment = ""
            iea_segment = ""
        elif error_target == "isa_missing_delimiter":
            # Remove a random "*" from ISA segment
            asterisk_positions = [i for i, char in enumerate(isa_segment) if char == "*"]
            if asterisk_positions:
                pos_to_remove = random.choice(asterisk_positions)
                isa_segment = isa_segment[:pos_to_remove] + isa_segment[pos_to_remove+1:]
        elif error_target == "isa_extra_delimiter":
            # Add an extra "*" to ISA segment
            asterisk_positions = [i for i, char in enumerate(isa_segment) if char == "*"]
            if asterisk_positions:
                pos_to_duplicate = random.choice(asterisk_positions)
                isa_segment = isa_segment[:pos_to_duplicate] + "*" + isa_segment[pos_to_duplicate:]
        elif error_target == "isa_missing_terminator":
            # Remove the final "~" from ISA segment
            isa_segment = isa_segment.rstrip("~")
        elif error_target == "isa_missing_field":
            # Remove a random field from ISA segment
            fields = isa_segment.split("*")
            if len(fields) > 0:
                fields.pop(random.randint(0, len(fields)-1))
                isa_segment = "*".join(fields)
        elif error_target == "isa_blank_field":
            # Make a random field blank in ISA segment
            fields = isa_segment.split("*")
            if len(fields) > 0:
                fields[random.randint(0, len(fields)-1)] = ""
                isa_segment = "*".join(fields)
        elif error_target == "iea_missing_delimiter":
            # Remove a random "*" from IEA segment
            asterisk_positions = [i for i, char in enumerate(iea_segment) if char == "*"]
            if asterisk_positions:
                pos_to_remove = random.choice(asterisk_positions)
                iea_segment = iea_segment[:pos_to_remove] + iea_segment[pos_to_remove+1:]
        elif error_target == "iea_extra_delimiter":
            # Add an extra "*" to IEA segment
            asterisk_positions = [i for i, char in enumerate(iea_segment) if char == "*"]
            if asterisk_positions:
                pos_to_duplicate = random.choice(asterisk_positions)
                iea_segment = iea_segment[:pos_to_duplicate] + "*" + iea_segment[pos_to_duplicate:]
        elif error_target == "iea_missing_terminator":
            # Remove the final "~" from IEA segment
            iea_segment = iea_segment.rstrip("~")
        elif error_target == "iea_missing_field":
            # Remove a random field from IEA segment
            fields = iea_segment.split("*")
            if len(fields) > 0:
                fields.pop(random.randint(0, len(fields)-1))
                iea_segment = "*".join(fields)
        elif error_target == "iea_blank_field":
            # Make a random field blank in IEA segment
            fields = iea_segment.split("*")
            if len(fields) > 0:
                fields[random.randint(0, len(fields)-1)] = ""
                iea_segment = "*".join(fields)
        elif error_target == "mismatched_control":
            # Generate a different control number
            incorrect_control_number = generate_control_number(with_errors=False)
            iea_segment = f"IEA*{group_count}*{incorrect_control_number}~"
        elif error_target == "incorrect_group_count":
            # Generate a different group count            
            incorrect_count = random.randint(0, 1000)
            iea_segment = f"IEA*{incorrect_count}*{control_number}~"
    
    # Return error info for error explanations
    error_info = None
    if with_errors:
        from core.field_generators import get_error_explanation
        explanation = get_error_explanation(error_target, "", "")
        error_info = {
            "error_type": error_type,
            "error_target": error_target,
            "explanation": explanation
        }
    
    # Return dictionary with segments and shared data
    return {
        "isa_segment": isa_segment,
        "iea_segment": iea_segment,
        "error_info": error_info,
        "shared_data": {
            "control_number": control_number,
            "group_count": group_count,
            "version": version,
            "date": date,
            "time": time,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "sender_qualifier": sender_qualifier,
            "receiver_qualifier": receiver_qualifier
        }
    }

