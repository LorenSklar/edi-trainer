"""
Error Field Generators

Systematic error generation for EDI fields. Creates realistic errors that follow
EDI patterns but use wrong values, lengths, or formats.
"""

from faker import Faker
import random
from typing import Union, List, Optional

fake = Faker()


def generate_wrong_field(
    field_type: str,
    correct_value: str = "",
    error_type: Optional[str] = None
) -> str:
    """
    Generate a wrong value for any EDI field type.
    
    Args:
        field_type: Type of field (date, time, version, id, code, etc.)
        correct_value: The correct value (for reference)
        error_type: Specific error type to generate (None = random)
    
    Returns:
        A wrong value that looks realistic but is invalid
    """
    if error_type is None:
        error_type = random.choice(["missing", "wrong_length", "wrong_format", "wrong_value"])
    
    if error_type == "missing":
        return ""
    
    if field_type == "date":
        return _generate_wrong_date(error_type)
    elif field_type == "time":
        return _generate_wrong_time(error_type)
    elif field_type == "version":
        return _generate_wrong_version(error_type)
    elif field_type == "id":
        return _generate_wrong_id(error_type, correct_value)
    elif field_type == "code":
        return _generate_wrong_code(error_type, correct_value)
    elif field_type == "ssn":
        return _generate_wrong_ssn(error_type)
    elif field_type == "control_number":
        return _generate_wrong_control_number(error_type)
    else:
        return _generate_wrong_generic(error_type, correct_value)


def _generate_wrong_date(error_type: str) -> str:
    """Generate wrong date formats"""
    if error_type == "wrong_format":
        return fake.date(pattern="%m/%d/%Y")  # Wrong format with slashes
    elif error_type == "wrong_length":
        return fake.date(pattern="%y%m%d")  # Wrong length (6 vs 8)
    else:  # wrong_value
        return fake.date(pattern="%Y%m%d")  # Future date (wrong value)


def _generate_wrong_time(error_type: str) -> str:
    """Generate wrong time formats"""
    if error_type == "wrong_format":
        return fake.time(pattern="%H:%M:%S")  # Wrong format with colons
    elif error_type == "wrong_length":
        return fake.time(pattern="%H%M")  # Wrong length (4 vs 6)
    else:  # wrong_value
        return fake.time(pattern="%H%M%S")  # Valid format but wrong time


def _generate_wrong_version(error_type: str) -> str:
    """Generate wrong EDI versions"""
    if error_type == "wrong_value":
        # Completely different transaction versions
        return fake.random_element(elements=(
            "004010X096A1",  # 4010 835 version
            "003010X096A1",  # 3010 version
            "005010X222A1",  # 5010 835 version
            "005010X330A1",  # 5010 837 version
            "005010X220B3"   # Wrong 834 version
        ))
    elif error_type == "wrong_length":
        # Wrong length versions
        return fake.random_element(elements=(
            "005010X220A",   # Too short
            "005010X220A10", # Too long
            "005010X220A1X"  # Extra character
        ))
    else:  # wrong_format
        # Malformed versions
        return fake.random_element(elements=(
            "005010X220A-1", # With dash
            "005010X220A.1", # With dot
            "005010X220A1 "  # With space
        ))


def _generate_wrong_id(error_type: str, correct_value: str) -> str:
    """Generate wrong IDs (sender, receiver, etc.)"""
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        # Generate alphanumeric with wrong length
        if len(correct_value) > 10:
            # Too long
            return fake.bothify(text="?" * 20, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        else:
            # Too short
            return fake.bothify(text="?" * 3, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    elif error_type == "wrong_format":
        # Invalid characters
        return fake.bothify(text="?" * len(correct_value), letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%")
    else:  # wrong_value
        # Valid format, wrong value
        return fake.bothify(text="?" * len(correct_value), letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def _generate_wrong_code(error_type: str, correct_value: str) -> str:
    """Generate wrong codes (maintenance type, relationship, etc.)"""
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        # Wrong length codes
        if len(correct_value) == 2:
            return fake.bothify(text="?", letters="0123456789")  # Too short
        else:
            return fake.bothify(text="??", letters="0123456789")  # Too long
    elif error_type == "wrong_format":
        # Invalid format
        return fake.bothify(text="?" * len(correct_value), letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    else:  # wrong_value
        # Valid format, wrong value
        return fake.bothify(text="?" * len(correct_value), letters="0123456789")


def _generate_wrong_ssn(error_type: str) -> str:
    """Generate wrong SSNs"""
    if error_type == "missing":
        return ""
    elif error_type == "wrong_format":
        # With dashes (wrong for EDI)
        return fake.ssn()
    elif error_type == "wrong_length":
        # Wrong length
        return fake.bothify(text="?" * 8, letters="0123456789")  # Too short
    else:  # wrong_value
        # Invalid SSN patterns
        return fake.random_element(elements=(
            "000-00-0000",
            "999-99-9999",
            "123-45-6789"
        )).replace("-", "")


def _generate_wrong_control_number(error_type: str) -> str:
    """Generate wrong control numbers"""
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        # Wrong length
        return fake.bothify(text="?" * 3, letters="0123456789")  # Too short
    elif error_type == "wrong_format":
        # With letters (wrong format)
        return fake.bothify(text="?" * 9, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    else:  # wrong_value
        # Valid format, wrong value
        return fake.bothify(text="?" * 9, letters="0123456789")


def _generate_wrong_generic(error_type: str, correct_value: str) -> str:
    """Generate wrong values for generic fields"""
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        # Wrong length
        if len(correct_value) > 5:
            return fake.bothify(text="?" * 2, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        else:
            return fake.bothify(text="?" * 10, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    elif error_type == "wrong_format":
        # Invalid characters
        return fake.bothify(text="?" * len(correct_value), letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%")
    else:  # wrong_value
        # Valid format, wrong value
        return fake.bothify(text="?" * len(correct_value), letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")


def get_error_explanation(field_type: str, error_type: str, field_name: str) -> str:
    """
    Get GRR explanation for why a field is wrong.
    
    Args:
        field_type: Type of field (date, time, version, etc.)
        error_type: Type of error (missing, wrong_length, etc.)
        field_name: Human-readable field name
    
    Returns:
        Explanation of the error
    """
    explanations = {
        "missing": f"The {field_name} field is required but is missing.",
        "wrong_length": f"The {field_name} field has the wrong length.",
        "wrong_format": f"The {field_name} field has an invalid format.",
        "wrong_value": f"The {field_name} field contains an invalid value."
    }
    
    base_explanation = explanations.get(error_type, f"The {field_name} field is invalid.")
    
    # Add field-specific details
    if field_type == "date":
        base_explanation += " EDI dates must be in CCYYMMDD format (8 digits, no separators)."
    elif field_type == "time":
        base_explanation += " EDI times must be in HHMMSS format (6 digits, no separators)."
    elif field_type == "version":
        base_explanation += " The version must match the transaction type (834 uses 005010X220A1)."
    elif field_type == "ssn":
        base_explanation += " SSNs must be exactly 9 digits with no dashes or spaces."
    
    return base_explanation
