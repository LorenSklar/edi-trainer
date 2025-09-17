"""
Tests for field generators module.

Tests all field generation functions for both clean and error-filled data.
"""

import pytest
from src.core.field_generators import (
    generate_sender_id, generate_receiver_id, generate_date, generate_time,
    generate_control_number, generate_group_count, generate_sender_qualifier,
    generate_receiver_qualifier, generate_version, generate_acknowledgment_code,
    generate_usage_indicator, get_error_explanation
)


class TestFieldGenerators:
    """Test individual field generators."""
    
    def test_generate_sender_id_clean(self):
        """Test clean sender ID generation."""
        sender_id = generate_sender_id(with_errors=False)
        assert len(sender_id) == 15
        assert sender_id.strip() != ""  # Should not be empty or just spaces
        assert sender_id.endswith(" ")  # Should be padded to 15 chars
    
    def test_generate_sender_id_with_errors(self):
        """Test sender ID generation with errors."""
        # Run multiple times to catch different error types
        for _ in range(10):
            sender_id = generate_sender_id(with_errors=True)
            # Should still be 15 characters (fixed width)
            assert len(sender_id) == 15
    
    def test_generate_receiver_id_clean(self):
        """Test clean receiver ID generation."""
        receiver_id = generate_receiver_id(with_errors=False)
        assert len(receiver_id) == 15
        assert receiver_id.strip() != ""
        assert receiver_id.endswith(" ")
    
    def test_generate_receiver_id_with_errors(self):
        """Test receiver ID generation with errors."""
        for _ in range(10):
            receiver_id = generate_receiver_id(with_errors=True)
            assert len(receiver_id) == 15
    
    def test_generate_date_clean(self):
        """Test clean date generation."""
        date = generate_date(with_errors=False)
        assert len(date) == 6
        assert date.isdigit()
        # Should be in YYMMDD format
        assert int(date[:2]) >= 70  # Year should be 1970 or later
        assert 1 <= int(date[2:4]) <= 12  # Month should be 01-12
        assert 1 <= int(date[4:6]) <= 31  # Day should be 01-31
    
    def test_generate_date_with_errors(self):
        """Test date generation with errors."""
        for _ in range(10):
            date = generate_date(with_errors=True)
            # Should still be 6 characters
            assert len(date) == 6
    
    def test_generate_time_clean(self):
        """Test clean time generation."""
        time = generate_time(with_errors=False)
        assert len(time) == 4
        assert time.isdigit()
        # Should be in HHMM format
        assert 0 <= int(time[:2]) <= 23  # Hour should be 00-23
        assert 0 <= int(time[2:4]) <= 59  # Minutes should be 00-59
    
    def test_generate_time_with_errors(self):
        """Test time generation with errors."""
        for _ in range(10):
            time = generate_time(with_errors=True)
            assert len(time) == 4
    
    def test_generate_control_number_clean(self):
        """Test clean control number generation."""
        control_number = generate_control_number(with_errors=False)
        assert len(control_number) == 9
        assert control_number.isdigit()
        assert control_number.startswith("0000000")  # Should be zero-padded
    
    def test_generate_control_number_with_errors(self):
        """Test control number generation with errors."""
        for _ in range(10):
            control_number = generate_control_number(with_errors=True)
            assert len(control_number) == 9
    
    def test_generate_group_count_clean(self):
        """Test clean group count generation."""
        group_count = generate_group_count(with_errors=False)
        assert group_count.isdigit()
        assert 1 <= int(group_count) <= 5  # Should be 1-5 digits
        assert int(group_count) >= 1  # Should be at least 1
    
    def test_generate_group_count_with_errors(self):
        """Test group count generation with errors."""
        for _ in range(10):
            group_count = generate_group_count(with_errors=True)
            assert group_count.isdigit()
    
    def test_generate_sender_qualifier_clean(self):
        """Test clean sender qualifier generation."""
        qualifier = generate_sender_qualifier(with_errors=False)
        assert qualifier == "ZZ"  # Should default to ZZ
    
    def test_generate_sender_qualifier_with_errors(self):
        """Test sender qualifier generation with errors."""
        for _ in range(10):
            qualifier = generate_sender_qualifier(with_errors=True)
            assert len(qualifier) == 2
            # Should be either wrong qualifier or invalid value
            assert qualifier in ["12", "30", "31", "32", "XX", "99", "ZZZ", "AB"]
    
    def test_generate_receiver_qualifier_clean(self):
        """Test clean receiver qualifier generation."""
        qualifier = generate_receiver_qualifier(with_errors=False)
        assert qualifier == "ZZ"
    
    def test_generate_receiver_qualifier_with_errors(self):
        """Test receiver qualifier generation with errors."""
        for _ in range(10):
            qualifier = generate_receiver_qualifier(with_errors=True)
            assert len(qualifier) == 2
            assert qualifier in ["12", "30", "31", "32", "XX", "99", "ZZZ", "AB"]
    
    def test_generate_version_clean(self):
        """Test clean version generation."""
        version = generate_version(with_errors=False)
        assert version == "00501"  # Should default to current standard
    
    def test_generate_version_with_errors(self):
        """Test version generation with errors."""
        for _ in range(10):
            version = generate_version(with_errors=True)
            assert len(version) == 5
            # Should be either old version or invalid version
            assert version in ["00401", "00301", "00201", "00502", "00601", "99999", "V501"]
    
    def test_generate_acknowledgment_code_clean(self):
        """Test clean acknowledgment code generation."""
        ack = generate_acknowledgment_code(with_errors=False)
        assert ack == "0"  # Should default to no acknowledgment
    
    def test_generate_acknowledgment_code_with_errors(self):
        """Test acknowledgment code generation with errors."""
        for _ in range(10):
            ack = generate_acknowledgment_code(with_errors=True)
            assert len(ack) >= 1
            # Should be either boolean-style or invalid value
            assert ack in ["T", "F", "TRUE", "FALSE", "Y", "N", "Yes", "No", "2", "X", "A", "R"]
    
    def test_generate_usage_indicator_clean(self):
        """Test clean usage indicator generation."""
        usage = generate_usage_indicator(with_errors=False)
        assert usage == "P"  # Should default to Production
    
    def test_generate_usage_indicator_with_errors(self):
        """Test usage indicator generation with errors."""
        for _ in range(10):
            usage = generate_usage_indicator(with_errors=True)
            assert len(usage) >= 1
            # Should be either staging codes or invalid value
            assert usage in ["S", "Q", "D", "U", "X", "1", "0", "PROD", "TEST"]


class TestErrorExplanations:
    """Test error explanation functionality."""
    
    def test_get_error_explanation_missing(self):
        """Test error explanation for missing field."""
        explanation = get_error_explanation("Test Field", "", "alphanumeric")
        assert "missing" in explanation.lower()
        assert "required" in explanation.lower()
    
    def test_get_error_explanation_wrong_length(self):
        """Test error explanation for wrong length."""
        explanation = get_error_explanation("Test Field", "123", "alphanumeric")
        assert "length" in explanation.lower()
        assert "wrong" in explanation.lower()
    
    def test_get_error_explanation_invalid_characters(self):
        """Test error explanation for invalid characters."""
        explanation = get_error_explanation("Test Field", "test@#$", "alphanumeric")
        assert "invalid" in explanation.lower()
        assert "characters" in explanation.lower()
    
    def test_get_error_explanation_numeric_field_with_letters(self):
        """Test error explanation for numeric field with letters."""
        explanation = get_error_explanation("Control Number", "abc123", "numeric")
        assert "letters" in explanation.lower()
        assert "numeric" in explanation.lower()


class TestFieldConsistency:
    """Test field generation consistency."""
    
    def test_all_fields_generate_consistently(self):
        """Test that all field generators work without errors."""
        # Generate all fields multiple times to ensure consistency
        for _ in range(5):
            sender_id = generate_sender_id(with_errors=False)
            receiver_id = generate_receiver_id(with_errors=False)
            date = generate_date(with_errors=False)
            time = generate_time(with_errors=False)
            control_number = generate_control_number(with_errors=False)
            group_count = generate_group_count(with_errors=False)
            sender_qual = generate_sender_qualifier(with_errors=False)
            receiver_qual = generate_receiver_qualifier(with_errors=False)
            version = generate_version(with_errors=False)
            ack = generate_acknowledgment_code(with_errors=False)
            usage = generate_usage_indicator(with_errors=False)
            
            # All should generate without errors
            assert all([sender_id, receiver_id, date, time, control_number, 
                       group_count, sender_qual, receiver_qual, version, ack, usage])
    
    def test_error_generation_variety(self):
        """Test that error generation produces variety."""
        # Generate multiple error-filled fields and ensure we get different results
        sender_ids = [generate_sender_id(with_errors=True) for _ in range(20)]
        receiver_ids = [generate_receiver_id(with_errors=True) for _ in range(20)]
        
        # Should have some variety (not all identical)
        assert len(set(sender_ids)) > 1
        assert len(set(receiver_ids)) > 1
