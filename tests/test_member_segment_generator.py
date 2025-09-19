#!/usr/bin/env python3
"""
Test Member Segment Generator

Tests the generation of member segments (NM1, PER, N3, N4, DMG)
with focus on YAML validation rules loading and field structure.
"""

import sys
import os
import yaml

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.member_segment_generator import (
    generate_nm1_segment,
    generate_per_segment,
    generate_n3_segment,
    generate_n4_segment,
    generate_dmg_segment,
    generate_member_data
)

def load_member_yaml_specs():
    """Load member segment specifications from YAML file."""
    yaml_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'member_segment_specifications.yaml')
    
    try:
        with open(yaml_path, 'r') as file:
            specs = yaml.safe_load(file)
        return specs
    except FileNotFoundError:
        print(f"❌ YAML file not found: {yaml_path}")
        return None
    except yaml.YAMLError as e:
        print(f"❌ YAML parsing error: {e}")
        return None

def test_yaml_loading():
    """Test that member YAML specifications can be loaded."""
    print("Testing member YAML specifications loading...")
    
    specs = load_member_yaml_specs()
    
    if specs is None:
        print("⚠️  Member YAML file not found or invalid - skipping YAML-based tests")
        return False
    
    # Check for basic structure
    assert isinstance(specs, dict), "YAML should be a dictionary"
    
    # Check for segments section
    if 'segments' not in specs:
        print("⚠️  No 'segments' section found in YAML - validation rules not available")
        return False
    
    # Check for fields section
    if 'fields' not in specs:
        print("⚠️  No 'fields' section found in YAML - field validation rules not available")
        return False
    
    # Check for validation_rules section
    if 'validation_rules' not in specs:
        print("⚠️  No 'validation_rules' section found in YAML - validation rules not available")
        return False
    
    print("✅ Member YAML specifications loaded successfully")
    return True

def test_member_segment_structure():
    """Test that member segments have correct structure."""
    print("Testing member segment structure...")
    
    # Test NM1 segment
    nm1_segment = generate_nm1_segment()
    assert nm1_segment.startswith("NM1*"), f"NM1 segment should start with 'NM1*', got: {nm1_segment}"
    assert nm1_segment.endswith("~"), f"NM1 segment should end with '~', got: {nm1_segment}"
    
    # Test PER segment
    per_segment = generate_per_segment()
    assert per_segment.startswith("PER*"), f"PER segment should start with 'PER*', got: {per_segment}"
    assert per_segment.endswith("~"), f"PER segment should end with '~', got: {per_segment}"
    
    # Test N3 segment
    n3_segment = generate_n3_segment()
    assert n3_segment.startswith("N3*"), f"N3 segment should start with 'N3*', got: {n3_segment}"
    assert n3_segment.endswith("~"), f"N3 segment should end with '~', got: {n3_segment}"
    
    # Test N4 segment
    n4_segment = generate_n4_segment()
    assert n4_segment.startswith("N4*"), f"N4 segment should start with 'N4*', got: {n4_segment}"
    assert n4_segment.endswith("~"), f"N4 segment should end with '~', got: {n4_segment}"
    
    # Test DMG segment
    dmg_segment = generate_dmg_segment()
    assert dmg_segment.startswith("DMG*"), f"DMG segment should start with 'DMG*', got: {dmg_segment}"
    assert dmg_segment.endswith("~"), f"DMG segment should end with '~', got: {dmg_segment}"
    
    print("✅ All member segments have correct structure")

def test_member_data_generation():
    """Test that member data generation works correctly."""
    print("Testing member data generation...")
    
    member_data = generate_member_data()
    
    # Check that all expected segments are present
    expected_segments = ["nm1", "per_segments", "n3_segments", "n4_segments", "dmg_segments"]
    for segment_type in expected_segments:
        assert segment_type in member_data, f"Member data should contain {segment_type}"
        assert isinstance(member_data[segment_type], list), f"{segment_type} should be a list"
        assert len(member_data[segment_type]) > 0, f"{segment_type} should not be empty"
    
    # Check that segments are valid
    for segment in member_data["nm1"]:
        assert segment.startswith("NM1*"), f"NM1 segment should start with 'NM1*', got: {segment}"
    
    for segment in member_data["per_segments"]:
        assert segment.startswith("PER*"), f"PER segment should start with 'PER*', got: {segment}"
    
    print("✅ Member data generation works correctly")

def test_yaml_validation_rules():
    """Test YAML validation rules if available."""
    print("Testing YAML validation rules...")
    
    specs = load_member_yaml_specs()
    
    if specs is None or 'validation_rules' not in specs:
        print("⚠️  Skipping YAML validation rules test - no rules available")
        return
    
    validation_rules = specs['validation_rules']
    assert isinstance(validation_rules, dict), "Validation rules should be a dictionary"
    
    # Check for common validation rule types
    rule_types = [
        'transaction_begins_with_nm1',
        'nm1_field_count',
        'per_field_count',
        'n3_field_count',
        'n4_field_count',
        'dmg_field_count',
        'segment_terminator',
        'field_separator'
    ]
    
    found_rules = []
    for rule_type in rule_types:
        if rule_type in validation_rules:
            found_rules.append(rule_type)
    
    if found_rules:
        print(f"✅ Found {len(found_rules)} validation rules: {', '.join(found_rules)}")
    else:
        print("⚠️  No standard validation rules found in YAML")

def test_field_validation_rules():
    """Test field validation rules if available."""
    print("Testing field validation rules...")
    
    specs = load_member_yaml_specs()
    
    if specs is None or 'fields' not in specs:
        print("⚠️  Skipping field validation rules test - no field rules available")
        return
    
    fields = specs['fields']
    assert isinstance(fields, dict), "Fields should be a dictionary"
    
    # Check for common member fields
    expected_fields = ['NM101', 'NM102', 'NM103', 'NM104', 'PER01', 'PER02', 'N301', 'N302', 'N401', 'N402', 'DMG01', 'DMG02', 'DMG03']
    
    found_fields = []
    for field in expected_fields:
        if field in fields:
            found_fields.append(field)
    
    if found_fields:
        print(f"✅ Found {len(found_fields)} field definitions: {', '.join(found_fields)}")
        
        # Test a few field definitions
        for field_name in found_fields[:3]:  # Test first 3 fields
            field_def = fields[field_name]
            assert 'name' in field_def, f"Field {field_name} should have 'name'"
            assert 'rules' in field_def, f"Field {field_name} should have 'rules'"
            print(f"  - {field_name}: {field_def['name']}")
    else:
        print("⚠️  No standard field definitions found in YAML")

def test_edi_delimiter_safety():
    """Test that field content doesn't contain EDI delimiter characters."""
    print("Testing EDI delimiter safety...")
    
    # EDI delimiter characters that should NOT appear in field content
    edi_delimiters = "*~:>+^"
    
    # Test member segments
    member_data = generate_member_data()
    
    for segment_type, segments in member_data.items():
        for segment in segments:
            # Extract field content (between * delimiters, excluding segment identifier)
            fields = segment.split("*")[1:]  # Skip segment identifier
            for field in fields:
                field_content = field.rstrip("~")  # Remove segment terminator
                for delimiter in edi_delimiters:
                    assert delimiter not in field_content, f"Field content contains delimiter '{delimiter}': {repr(field_content)}"
    
    print("✅ No EDI delimiters found in field content")

def main():
    """Run all member segment generator tests."""
    print("🧪 Testing Member Segment Generator")
    print("===================================")
    
    try:
        yaml_loaded = test_yaml_loading()
        test_member_segment_structure()
        test_member_data_generation()
        
        if yaml_loaded:
            test_yaml_validation_rules()
            test_field_validation_rules()
        
        test_edi_delimiter_safety()
        
        print("\n🎉 All member segment generator tests passed!")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
