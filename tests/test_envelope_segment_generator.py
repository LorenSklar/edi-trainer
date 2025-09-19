#!/usr/bin/env python3
"""
Test Envelope Segment Generator

Tests the generation of envelope segments (ISA, IEA, GS, GE, ST, SE, BGN)
with focus on ISA/IEA control number matching and proper field structure.
"""

import sys
import os

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.envelope_segment_generator import (
    generate_isa_segment, 
    generate_iea_segment, 
    generate_envelope_data
)

def test_isa_segment_structure():
    """Test that ISA segment has correct structure (16 fields)."""
    print("Testing ISA segment structure...")
    
    isa_segment = generate_isa_segment()
    
    # Check that it starts with ISA
    assert isa_segment.startswith("ISA*"), f"ISA segment should start with 'ISA*', got: {isa_segment}"
    
    # Check that it ends with ~
    assert isa_segment.endswith("~"), f"ISA segment should end with '~', got: {isa_segment}"
    
    # Split by * and check field count
    fields = isa_segment.split("*")
    assert len(fields) == 17, f"ISA should have 17 parts (ISA + 16 fields), got: {len(fields)}"
    
    # Check that ISA13 (control number) is 9 digits
    isa13 = fields[13]
    assert len(isa13) == 9, f"ISA13 (control number) should be 9 digits, got: {len(isa13)}"
    assert isa13.isdigit(), f"ISA13 (control number) should be numeric, got: {isa13}"
    
    print(f"✅ ISA segment structure correct: {len(fields)-1} fields")
    return isa_segment

def test_iea_segment_structure():
    """Test that IEA segment has correct structure (2 fields)."""
    print("Testing IEA segment structure...")
    
    iea_segment = generate_iea_segment()
    
    # Check that it starts with IEA
    assert iea_segment.startswith("IEA*"), f"IEA segment should start with 'IEA*', got: {iea_segment}"
    
    # Check that it ends with ~
    assert iea_segment.endswith("~"), f"IEA segment should end with '~', got: {iea_segment}"
    
    # Split by * and check field count
    fields = iea_segment.split("*")
    assert len(fields) == 3, f"IEA should have 3 parts (IEA + 2 fields), got: {len(fields)}"
    
    # Check that IEA02 (control number) is 9 digits
    iea02 = fields[2].rstrip("~")
    assert len(iea02) == 9, f"IEA02 (control number) should be 9 digits, got: {len(iea02)}"
    assert iea02.isdigit(), f"IEA02 (control number) should be numeric, got: {iea02}"
    
    print(f"✅ IEA segment structure correct: {len(fields)-1} fields")
    return iea_segment

def test_control_number_matching():
    """Test that ISA13 and IEA02 control numbers match when generated together."""
    print("Testing control number matching...")
    
    # Generate envelope data which should create matching control numbers
    envelope_data = generate_envelope_data()
    
    isa_segment = envelope_data["isa"][0]
    iea_segment = envelope_data["iea"][0]
    
    # Extract control numbers
    isa_fields = isa_segment.split("*")
    iea_fields = iea_segment.split("*")
    
    isa13 = isa_fields[13]  # ISA13 control number
    iea02 = iea_fields[2].rstrip("~")  # IEA02 control number (remove trailing ~)
    
    assert isa13 == iea02, f"ISA13 ({isa13}) and IEA02 ({iea02}) control numbers should match"
    
    print(f"✅ Control numbers match: ISA13={isa13}, IEA02={iea02}")
    return isa13, iea02

def test_field_values():
    """Test that specific field values are generated correctly."""
    print("Testing field value generation...")
    
    # Generate ISA segment and extract fields
    isa_segment = generate_isa_segment()
    fields = isa_segment.split("*")
    
    # Extract specific fields (ISA01 is at index 1, ISA02 at index 2, etc.)
    isa01 = fields[1]   # Authorization qualifier
    isa02 = fields[2]   # Authorization info (should be 10 spaces)
    isa06 = fields[6]   # Sender ID
    isa09 = fields[9]   # Interchange date
    isa10 = fields[10]  # Interchange time
    
    # Check ISA02 (authorization info) is 10 spaces
    assert isa02 == "          ", f"ISA02 should be 10 spaces, got: {repr(isa02)}"
    
    # Check ISA06 (sender ID) is right-padded to 15 characters
    assert len(isa06) == 15, f"ISA06 should be 15 characters, got: {len(isa06)}"
    
    # Check ISA09 (date) is 6 digits
    assert len(isa09) == 6, f"ISA09 should be 6 digits, got: {len(isa09)}"
    assert isa09.isdigit(), f"ISA09 should be numeric, got: {isa09}"
    
    # Check ISA10 (time) is 4 digits
    assert len(isa10) == 4, f"ISA10 should be 4 digits, got: {len(isa10)}"
    assert isa10.isdigit(), f"ISA10 should be numeric, got: {isa10}"
    
    print(f"✅ Field values correct: ISA01={isa01}, ISA02={repr(isa02)}, ISA06={repr(isa06)}, ISA09={isa09}, ISA10={isa10}")

def test_edi_delimiter_safety():
    """Test that field content doesn't contain EDI delimiter characters."""
    print("Testing EDI delimiter safety...")
    
    # EDI delimiter characters that should NOT appear in field content
    edi_delimiters = "*~:>+^"
    
    # Generate ISA segment and test content fields
    isa_segment = generate_isa_segment()
    fields = isa_segment.split("*")
    
    # Test content fields (not delimiter fields)
    # ISA06 (index 6) and ISA08 (index 8) are Company ID fields
    content_fields = [
        ("ISA06", fields[6]),   # Sender ID
        ("ISA08", fields[8])    # Receiver ID
    ]
    
    for field_name, value in content_fields:
        for delimiter in edi_delimiters:
            assert delimiter not in value, f"Field {field_name} contains delimiter '{delimiter}': {repr(value)}"
    
    print("✅ No EDI delimiters found in field content")

def test_multiple_generations():
    """Test that multiple generations produce different values."""
    print("Testing multiple generations...")
    
    # Generate multiple ISA segments and check they're different
    isa1 = generate_isa_segment()
    isa2 = generate_isa_segment()
    
    # They should be different (random generation)
    assert isa1 != isa2, "Multiple ISA generations should produce different results"
    
    # But control numbers within envelope_data should match
    envelope1 = generate_envelope_data()
    envelope2 = generate_envelope_data()
    
    isa1_control = envelope1["isa"][0].split("*")[13]
    iea1_control = envelope1["iea"][0].split("*")[2].rstrip("~")
    
    isa2_control = envelope2["isa"][0].split("*")[13]
    iea2_control = envelope2["iea"][0].split("*")[2].rstrip("~")
    
    assert isa1_control == iea1_control, "Control numbers should match within same envelope"
    assert isa2_control == iea2_control, "Control numbers should match within same envelope"
    
    print("✅ Multiple generations work correctly")

def main():
    """Run all envelope segment generator tests."""
    print("🧪 Testing Envelope Segment Generator")
    print("====================================")
    
    try:
        test_isa_segment_structure()
        test_iea_segment_structure()
        test_control_number_matching()
        test_field_values()
        test_edi_delimiter_safety()
        test_multiple_generations()
        
        print("\n🎉 All envelope segment generator tests passed!")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
