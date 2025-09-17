"""
EDI Field Generators

Systematic field generation for EDI with realistic error prevalence.
Each function generates a specific field type with optional error injection.
"""

from faker import Faker
import random

fake = Faker()


def generate_sender_id(with_errors: bool = False) -> str:
    """Generate sender ID with realistic error prevalence"""
    if not with_errors:
        return fake.random_element(elements=("SENDER", "COMPANY", "HR_SYS"))
    
    # Realistic error prevalence: missing=40%, wrong_length=30%, wrong_format=20%, invalid_value=10%
    error_type = random.choices(
        ["missing", "wrong_length", "wrong_format", "invalid_value"],
        weights=[40, 30, 20, 10]
    )[0]
    
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        return fake.bothify(text="?" * 20, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Too long
    elif error_type == "wrong_format":
        return fake.bothify(text="?" * 8, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%")  # Invalid chars
    else:  # invalid_value
        return fake.bothify(text="?" * 8, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Valid format, wrong value


def generate_receiver_id(with_errors: bool = False) -> str:
    """Generate receiver ID with realistic error prevalence"""
    if not with_errors:
        return fake.random_element(elements=("RECEIVER", "CARRIER", "BCBS"))
    
    # Realistic error prevalence: missing=40%, wrong_length=30%, wrong_format=20%, invalid_value=10%
    error_type = random.choices(
        ["missing", "wrong_length", "wrong_format", "invalid_value"],
        weights=[40, 30, 20, 10]
    )[0]
    
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        return fake.bothify(text="?" * 20, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Too long
    elif error_type == "wrong_format":
        return fake.bothify(text="?" * 8, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%")  # Invalid chars
    else:  # invalid_value
        return fake.bothify(text="?" * 8, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Valid format, wrong value


def generate_date(with_errors: bool = False) -> str:
    """Generate date with realistic error prevalence"""
    if not with_errors:
        return fake.date(pattern="%y%m%d")  # Correct YYMMDD format
    
    # Realistic error prevalence: missing=30%, wrong_length=25%, wrong_format=35%, invalid_value=10%
    error_type = random.choices(
        ["missing", "wrong_length", "wrong_format", "invalid_value"],
        weights=[30, 25, 35, 10]
    )[0]
    
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        return fake.date(pattern="%y%m%d")  # 6 digits instead of 8
    elif error_type == "wrong_format":
        return fake.date(pattern="%m/%d/%Y")  # With slashes
    else:  # invalid_value
        return fake.date(pattern="%Y%m%d")  # Future date


def generate_time(with_errors: bool = False) -> str:
    """Generate time with realistic error prevalence"""
    if not with_errors:
        return fake.time(pattern="%H%M")
    
    # Realistic error prevalence: missing=20%, wrong_length=30%, wrong_format=40%, invalid_value=10%
    error_type = random.choices(
        ["missing", "wrong_length", "wrong_format", "invalid_value"],
        weights=[20, 30, 40, 10]
    )[0]
    
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        return fake.time(pattern="%H%M%S")  # 6 digits instead of 4
    elif error_type == "wrong_format":
        return fake.time(pattern="%H:%M:%S")  # With colons
    else:  # invalid_value
        return fake.time(pattern="%H%M")  # Valid format, wrong time


def generate_control_number(with_errors: bool = False) -> str:
    """Generate control number with realistic error prevalence"""
    if not with_errors:
        return str(fake.random_number(digits=9))
    
    # Realistic error prevalence: missing=25%, wrong_length=35%, wrong_format=25%, invalid_value=15%
    error_type = random.choices(
        ["missing", "wrong_length", "wrong_format", "invalid_value"],
        weights=[25, 35, 25, 15]
    )[0]
    
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        return fake.bothify(text="?" * 3, letters="0123456789")  # Too short
    elif error_type == "wrong_format":
        return fake.bothify(text="?" * 9, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")  # With letters
    else:  # invalid_value
        return fake.bothify(text="?" * 9, letters="0123456789")  # Valid format, wrong value


def generate_group_count(with_errors: bool = False) -> str:
    """Generate group count with realistic error prevalence"""
    if not with_errors:
        return "1"
    
    # Realistic error prevalence: missing=40%, wrong_length=20%, wrong_format=20%, invalid_value=20%
    error_type = random.choices(
        ["missing", "wrong_length", "wrong_format", "invalid_value"],
        weights=[40, 20, 20, 20]
    )[0]
    
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        return fake.bothify(text="?" * 3, letters="0123456789")  # Too long
    elif error_type == "wrong_format":
        return fake.bothify(text="?", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # With letters
    else:  # invalid_value
        return fake.bothify(text="?", letters="0123456789")  # Valid format, wrong value


def generate_segment_structure_error(segment: str, error_type: str) -> str:
    """
    Generate structural errors in EDI segments.
    
    Args:
        segment: The clean segment
        error_type: Type of structural error to introduce
    
    Returns:
        Segment with structural error
    """
    if error_type == "missing_delimiter":
        # Remove a random delimiter (but not the first or last)
        fields = segment.split('*')
        if len(fields) > 2:
            # Remove delimiter between random adjacent fields
            pos = random.randint(1, len(fields) - 2)
            fields[pos] = fields[pos] + fields[pos + 1]
            fields.pop(pos + 1)
            return '*'.join(fields)
        return segment
    
    elif error_type == "extra_delimiter":
        # Add an extra delimiter
        fields = segment.split('*')
        if len(fields) > 1:
            # Add empty field at random position
            pos = random.randint(1, len(fields) - 1)
            fields.insert(pos, "")
            return '*'.join(fields)
        return segment
    
    elif error_type == "missing_terminator":
        # Remove the segment terminator
        return segment.rstrip('~')
    
    elif error_type == "extra_terminator":
        # Add extra terminator
        return segment + '~'
    
    elif error_type == "truncated":
        # Remove last few fields
        fields = segment.split('*')
        if len(fields) > 3:
            # Remove 1-3 fields from the end
            remove_count = random.randint(1, min(3, len(fields) - 2))
            fields = fields[:-remove_count]
            return '*'.join(fields) + '~'
        return segment
    
    return segment


def get_error_explanation(field_name: str, field_value: str, expected_format: str) -> str:
    """
    Get GRR explanation for why a field is wrong.
    
    Args:
        field_name: Human-readable field name
        field_value: The actual field value
        expected_format: Expected format description
    
    Returns:
        Explanation of the error
    """
    if not field_value or field_value.strip() == "":
        return f"The {field_name} field is required but is missing."
    
    if len(field_value) != len(expected_format.replace(" ", "")):
        return f"The {field_name} field has wrong length: {len(field_value)} characters. Expected: {expected_format}."
    
    if any(char in field_value for char in "@#$%"):
        return f"The {field_name} field contains invalid characters. Expected: {expected_format}."
    
    if any(char.isalpha() for char in field_value) and field_name in ["Control Number", "Group Count"]:
        return f"The {field_name} field contains letters. Expected: {expected_format}."
    
    return f"The {field_name} field contains an invalid value. Expected: {expected_format}."