"""
Tests for segment generators module.

Tests ISA/IEA pair generation, error handling, and structural integrity.
"""

import pytest
from src.core.segment_generators import (
    generate_isa_iea_pair, generate_isa_segment, generate_iea_segment,
    get_isa_iea_error_explanation
)


class TestISAIEAPairGeneration:
    """Test ISA/IEA pair generation."""
    
    def test_generate_isa_iea_pair_clean(self):
        """Test clean ISA/IEA pair generation."""
        result = generate_isa_iea_pair(with_errors=False)
        
        # Check return structure
        assert isinstance(result, dict)
        assert "isa_segment" in result
        assert "iea_segment" in result
        assert "error_info" in result
        assert "shared_data" in result
        
        # Check error info is None for clean generation
        assert result["error_info"] is None
        
        # Check segments are not empty
        assert result["isa_segment"] != ""
        assert result["iea_segment"] != ""
        
        # Check ISA segment structure
        isa_parts = result["isa_segment"].split("*")
        assert len(isa_parts) == 17  # ISA should have 16 fields + segment identifier
        assert isa_parts[0] == "ISA"
        assert isa_parts[-1].endswith("~")  # Should end with terminator
        
        # Check IEA segment structure
        iea_parts = result["iea_segment"].split("*")
        assert len(iea_parts) == 3  # IEA should have 2 fields + segment identifier
        assert iea_parts[0] == "IEA"
        assert iea_parts[-1].endswith("~")
        
        # Check shared data structure
        shared_data = result["shared_data"]
        required_fields = [
            "control_number", "group_count", "version", "date", "time",
            "sender_id", "receiver_id", "sender_qualifier", "receiver_qualifier"
        ]
        for field in required_fields:
            assert field in shared_data
            assert shared_data[field] is not None
    
    def test_generate_isa_iea_pair_with_errors(self):
        """Test ISA/IEA pair generation with errors."""
        # Run multiple times to catch different error types
        for _ in range(20):
            result = generate_isa_iea_pair(with_errors=True)
            
            # Should have error info
            assert result["error_info"] is not None
            assert "error_type" in result["error_info"]
            assert "error_target" in result["error_info"]
            assert "field_name" in result["error_info"]
            assert "segment" in result["error_info"]
            
            # Error type should be either field_error or structural_error
            assert result["error_info"]["error_type"] in ["field_error", "structural_error"]
            
            # Segment should be ISA or IEA
            assert result["error_info"]["segment"] in ["ISA", "IEA"]
    
    def test_control_number_matching(self):
        """Test that control numbers match between ISA and IEA."""
        result = generate_isa_iea_pair(with_errors=False)
        
        # Extract control numbers from segments
        isa_parts = result["isa_segment"].split("*")
        iea_parts = result["iea_segment"].split("*")
        
        isa_control = isa_parts[13]  # ISA13 is control number
        iea_control = iea_parts[2]   # IEA02 is control number
        
        # Control numbers should match
        assert isa_control == iea_control
        assert isa_control == result["shared_data"]["control_number"]
    
    def test_shared_data_consistency(self):
        """Test that shared data matches segment content."""
        result = generate_isa_iea_pair(with_errors=False)
        shared_data = result["shared_data"]
        
        # Extract fields from ISA segment
        isa_parts = result["isa_segment"].split("*")
        
        # Check that shared data matches ISA content
        assert isa_parts[5] == shared_data["sender_qualifier"]  # ISA05
        assert isa_parts[6] == shared_data["sender_id"]         # ISA06
        assert isa_parts[7] == shared_data["receiver_qualifier"] # ISA07
        assert isa_parts[8] == shared_data["receiver_id"]       # ISA08
        assert isa_parts[9] == shared_data["date"]              # ISA09
        assert isa_parts[10] == shared_data["time"]             # ISA10
        assert isa_parts[12] == shared_data["version"]          # ISA12
        assert isa_parts[13] == shared_data["control_number"]   # ISA13
        
        # Check IEA content
        iea_parts = result["iea_segment"].split("*")
        assert iea_parts[1] == shared_data["group_count"]       # IEA01
        assert iea_parts[2] == shared_data["control_number"]    # IEA02


class TestIndividualSegmentGeneration:
    """Test individual segment generation functions."""
    
    def test_generate_isa_segment(self):
        """Test ISA segment generation."""
        isa_segment = generate_isa_segment(with_errors=False)
        
        assert isinstance(isa_segment, str)
        assert isa_segment.startswith("ISA*")
        assert isa_segment.endswith("~")
        
        # Should have correct number of fields
        parts = isa_segment.split("*")
        assert len(parts) == 17
    
    def test_generate_iea_segment(self):
        """Test IEA segment generation."""
        iea_segment = generate_iea_segment(with_errors=False)
        
        assert isinstance(iea_segment, str)
        assert iea_segment.startswith("IEA*")
        assert iea_segment.endswith("~")
        
        # Should have correct number of fields
        parts = iea_segment.split("*")
        assert len(parts) == 3


class TestErrorTypes:
    """Test different error types."""
    
    def test_field_errors(self):
        """Test that field errors are generated."""
        field_errors_found = set()
        
        # Run many times to catch different field errors
        for _ in range(100):
            result = generate_isa_iea_pair(with_errors=True)
            if result["error_info"]["error_type"] == "field_error":
                field_errors_found.add(result["error_info"]["error_target"])
        
        # Should have found multiple field error types
        assert len(field_errors_found) > 5
        
        # Should include common field errors
        expected_errors = [
            "isa_sender_qualifier", "isa_sender_id", "isa_receiver_qualifier",
            "isa_receiver_id", "isa_date", "isa_time", "isa_version"
        ]
        for error in expected_errors:
            assert error in field_errors_found
    
    def test_structural_errors(self):
        """Test that structural errors are generated."""
        structural_errors_found = set()
        
        # Run many times to catch different structural errors
        for _ in range(100):
            result = generate_isa_iea_pair(with_errors=True)
            if result["error_info"]["error_type"] == "structural_error":
                structural_errors_found.add(result["error_info"]["error_target"])
        
        # Should have found structural errors
        assert len(structural_errors_found) > 0
        
        # Should include missing_entire_envelope (most common)
        assert "missing_entire_envelope" in structural_errors_found
    
    def test_missing_entire_envelope_error(self):
        """Test missing entire envelope error specifically."""
        found_missing_envelope = False
        
        # Run until we find this specific error
        for _ in range(200):
            result = generate_isa_iea_pair(with_errors=True)
            if (result["error_info"] and 
                result["error_info"]["error_target"] == "missing_entire_envelope"):
                found_missing_envelope = True
                # Both segments should be empty
                assert result["isa_segment"] == ""
                assert result["iea_segment"] == ""
                break
        
        assert found_missing_envelope, "Should eventually generate missing_entire_envelope error"
    
    def test_mismatched_control_error(self):
        """Test mismatched control number error."""
        found_mismatch = False
        
        # Run until we find this specific error
        for _ in range(200):
            result = generate_isa_iea_pair(with_errors=True)
            if (result["error_info"] and 
                result["error_info"]["error_target"] == "mismatched_control"):
                found_mismatch = True
                
                # Extract control numbers
                isa_parts = result["isa_segment"].split("*")
                iea_parts = result["iea_segment"].split("*")
                isa_control = isa_parts[13]
                iea_control = iea_parts[2]
                
                # Control numbers should be different
                assert isa_control != iea_control
                break
        
        assert found_mismatch, "Should eventually generate mismatched_control error"
    
    def test_incorrect_group_count_error(self):
        """Test incorrect group count error."""
        found_incorrect_count = False
        
        # Run until we find this specific error
        for _ in range(200):
            result = generate_isa_iea_pair(with_errors=True)
            if (result["error_info"] and 
                result["error_info"]["error_target"] == "incorrect_group_count"):
                found_incorrect_count = True
                
                # Extract group count from IEA
                iea_parts = result["iea_segment"].split("*")
                group_count = iea_parts[1]
                
                # Should be an incorrect count (not 1)
                assert group_count in ["0", "2", "3", "5", "10"]
                break
        
        assert found_incorrect_count, "Should eventually generate incorrect_group_count error"


class TestErrorExplanations:
    """Test error explanation functionality."""
    
    def test_get_isa_iea_error_explanation(self):
        """Test ISA/IEA error explanation function."""
        # Test with valid segments
        isa_segment = "ISA*00*          *00*          *ZZ*SENDER_ID      *ZZ*RECEIVER_ID    *250917*1430*^00501*000000001*0*P*:~"
        iea_segment = "IEA*1*000000001~"
        
        explanation = get_isa_iea_error_explanation(isa_segment, iea_segment)
        assert "no errors" in explanation.lower() or "valid" in explanation.lower()
    
    def test_error_explanation_with_mismatched_controls(self):
        """Test error explanation with mismatched control numbers."""
        isa_segment = "ISA*00*          *00*          *ZZ*SENDER_ID      *ZZ*RECEIVER_ID    *250917*1430*^00501*000000001*0*P*:~"
        iea_segment = "IEA*1*000000002~"  # Different control number
        
        explanation = get_isa_iea_error_explanation(isa_segment, iea_segment)
        assert "mismatch" in explanation.lower() or "match" in explanation.lower()


class TestDataConsistency:
    """Test data consistency across multiple generations."""
    
    def test_multiple_generations_consistency(self):
        """Test that multiple generations work consistently."""
        results = []
        
        # Generate multiple pairs
        for _ in range(10):
            result = generate_isa_iea_pair(with_errors=False)
            results.append(result)
            
            # Each should have proper structure
            assert isinstance(result, dict)
            assert "isa_segment" in result
            assert "iea_segment" in result
            assert "shared_data" in result
        
        # Should have generated different control numbers
        control_numbers = [r["shared_data"]["control_number"] for r in results]
        assert len(set(control_numbers)) > 1  # Should have variety
    
    def test_error_generation_distribution(self):
        """Test that error generation has reasonable distribution."""
        error_types = {"field_error": 0, "structural_error": 0}
        
        # Generate many pairs with errors
        for _ in range(200):
            result = generate_isa_iea_pair(with_errors=True)
            if result["error_info"]:
                error_type = result["error_info"]["error_type"]
                error_types[error_type] += 1
        
        # Should have both types of errors
        assert error_types["field_error"] > 0
        assert error_types["structural_error"] > 0
        
        # Field errors should be more common (70% vs 30%)
        total_errors = sum(error_types.values())
        field_error_ratio = error_types["field_error"] / total_errors
        assert 0.5 < field_error_ratio < 0.9  # Should be around 70%
