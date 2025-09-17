"""
EDI Field Generators

Systematic field generation for EDI with realistic error prevalence.
Each function generates a specific field type with optional error injection.

TODO - CRITICAL ISSUES TO FIX:
1. Field generators produce unrealistic errors (like "INVALID" strings)
2. They mistakenly "correct" errors for "EDI compliance" when the whole point is to generate errors
3. They use random.choice and fake.bothify with question marks instead of leveraging Faker's powerful realistic data generation
4. They pad/truncate errors back to correct lengths, defeating the purpose
5. Error explanations are too generic - can't distinguish between missing, wrong format, wrong length, and invalid value errors
6. Gives generic "missing" messages even when the field is clearly present

FIELD GENERATORS NEED TO BE COMPLETELY REBUILT to generate realistic, believable errors that actually violate EDI standards.
"""

from faker import Faker
import random

fake = Faker()


def generate_sender_id(with_errors: bool = False) -> str:
    """Generate sender ID with realistic error prevalence"""
    if not with_errors:
        # Generate valid ID and pad to 15 characters
        base_id = fake.random_element(elements=("SENDER", "COMPANY", "HR_SYS"))
        return f"{base_id:<15}"  # Left-align and pad with spaces to 15 chars
    
    # Realistic error prevalence: missing=40%, wrong_length=30%, wrong_format=20%, invalid_value=10%
    error_type = random.choices(
        ["missing", "wrong_length", "wrong_format", "invalid_value"],
        weights=[40, 30, 20, 10]
    )[0]
    
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        return fake.company()[:8]  # Too short (8 chars)
    elif error_type == "wrong_format":
        return fake.bothify(text="???????????????", letters="0123456789@#$%")  # Numbers and symbols
    else:  # invalid_value
        return fake.company()  # Real company name but wrong format


def generate_receiver_id(with_errors: bool = False) -> str:
    """Generate receiver ID with realistic error prevalence"""
    if not with_errors:
        # Generate valid ID and pad to 15 characters
        base_id = fake.random_element(elements=("RECEIVER", "CARRIER", "BCBS"))
        return f"{base_id:<15}"  # Left-align and pad with spaces to 15 chars
    
    # Realistic error prevalence: missing=40%, wrong_length=30%, wrong_format=20%, invalid_value=10%
    error_type = random.choices(
        ["missing", "wrong_length", "wrong_format", "invalid_value"],
        weights=[40, 30, 20, 10]
    )[0]
    
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        return fake.company()[:8]  # Too short (8 chars)
    elif error_type == "wrong_format":
        return fake.bothify(text="???????????????", letters="0123456789@#$%")  # Numbers and symbols
    else:  # invalid_value
        return fake.company()  # Real company name but wrong format


def generate_date(with_errors: bool = False) -> str:
    """Generate date with realistic error prevalence"""
    if not with_errors:
        # Generate date from 1970 onwards using datetime
        from datetime import datetime, timedelta
        start_date = datetime(1970, 1, 1)
        end_date = datetime.now()
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        return random_date.strftime("%y%m%d")
    
    # Realistic error prevalence: missing=30%, wrong_length=25%, wrong_format=35%, invalid_value=10%
    error_type = random.choices(
        ["missing", "wrong_length", "wrong_format", "invalid_value"],
        weights=[30, 25, 35, 10]
    )[0]
    
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        return fake.numerify(text="##")  # Too short (2 digits)
    elif error_type == "wrong_format":
        # Use Faker's date formats with separators - realistic but wrong format
        return fake.date(pattern="%m/%d/%Y").replace("/", "")  # Slash format
    else:  # invalid_value
        # Generate invalid months (13-99) and days (32-99)
        invalid_month = fake.random_int(min=13, max=99)
        invalid_day = fake.random_int(min=32, max=99)
        year = fake.random_int(min=70, max=99)
        return f"{year:02d}{invalid_month:02d}{invalid_day:02d}"


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
        return fake.numerify(text="##")  # Too short (2 digits)
    elif error_type == "wrong_format":
        # Use Faker's time formats with separators - realistic but wrong format
        return fake.time(pattern="%H:%M:%S").replace(":", "")  # Colon format
    else:  # invalid_value
        # Generate invalid hours (25-99) and minutes (60-99)
        invalid_hour = fake.random_int(min=25, max=99)
        invalid_minute = fake.random_int(min=60, max=99)
        return f"{invalid_hour:02d}{invalid_minute:02d}"


def generate_control_number(with_errors: bool = False) -> str:
    """Generate control number with realistic error prevalence"""
    if not with_errors:
        # Generate control number starting with 0000000 (7 zeros) + 2 random digits
        # This is more realistic for EDI control numbers
        last_two = fake.random_number(digits=2)
        return f"0000000{last_two:02d}"  # 7 zeros + 2 digits = 9 total
    
    # Realistic error prevalence: missing=25%, wrong_length=35%, wrong_format=25%, invalid_value=15%
    error_type = random.choices(
        ["missing", "wrong_length", "wrong_format", "invalid_value"],
        weights=[25, 35, 25, 15]
    )[0]
    
    if error_type == "missing":
        return ""
    elif error_type == "wrong_length":
        return fake.numerify(text="###")  # Too short (3 digits)
    elif error_type == "wrong_format":
        return fake.lexify(text="?????????", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Letters instead of numbers
    else:  # invalid_value
        return fake.numerify(text="##########")  # Too long (10 digits)


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
        return fake.numerify(text="###")  # Too long (3 digits)
    elif error_type == "wrong_format":
        return fake.lexify(text="?", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Letter instead of number
    else:  # invalid_value
        return fake.numerify(text="##")  # Too long (2 digits)


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


def generate_sender_qualifier(with_errors: bool = False) -> str:
    """Generate sender qualifier (ISA05)"""
    if not with_errors:
        return "ZZ"  # Most common for healthcare
    
    # Error prevalence: wrong_qualifier=60%, invalid_value=40%
    error_type = random.choices(
        ["wrong_qualifier", "invalid_value"],
        weights=[60, 40]
    )[0]
    
    if error_type == "wrong_qualifier":
        # Valid qualifiers but wrong for this context
        return random.choice(["12", "30", "31", "32"])
    else:  # invalid_value
        # Invalid qualifier codes
        return random.choice(["XX", "99", "ZZZ", "AB"])


def generate_receiver_qualifier(with_errors: bool = False) -> str:
    """Generate receiver qualifier (ISA07)"""
    if not with_errors:
        return "ZZ"  # Most common for healthcare
    
    # Error prevalence: wrong_qualifier=60%, invalid_value=40%
    error_type = random.choices(
        ["wrong_qualifier", "invalid_value"],
        weights=[60, 40]
    )[0]
    
    if error_type == "wrong_qualifier":
        # Valid qualifiers but wrong for this context
        return random.choice(["12", "30", "31", "32"])
    else:  # invalid_value
        # Invalid qualifier codes
        return random.choice(["XX", "99", "ZZZ", "AB"])


def generate_version(with_errors: bool = False) -> str:
    """Generate interchange control version (ISA12)"""
    if not with_errors:
        return "00501"  # Current standard
    
    # Error prevalence: old_version=70%, invalid_version=30%
    error_type = random.choices(
        ["old_version", "invalid_version"],
        weights=[70, 30]
    )[0]
    
    if error_type == "old_version":
        # Older but valid versions
        return random.choice(["00401", "00301", "00201"])
    else:  # invalid_version
        # Invalid version codes
        return random.choice(["00502", "00601", "99999", "V501"])


def generate_acknowledgment_code(with_errors: bool = False) -> str:
    """Generate acknowledgment requested (ISA14)"""
    if not with_errors:
        # Random pick between 0 and 1, with 0 more common
        return random.choices(["0", "1"], weights=[90, 10])[0]
    
    # Error: single pick from boolean values
    return random.choice(["Y", "N", "Yes", "No", "T", "F", "TRUE", "FALSE"])


def generate_usage_indicator(with_errors: bool = False) -> str:
    """Generate usage indicator (ISA15) - Test/Production"""
    if not with_errors:
        # Random pick between T and P, with T more common
        return random.choices(["T", "P"], weights=[80, 20])[0]
    
    # Error: single pick from invalid values
    return random.choice(["X", "1", "0", "PROD", "TEST", "S", "Q", "D", "U"])