#!/usr/bin/env python3
"""
Test Header Segment Generator

Tests the generation of header segments (BGN, N1, REF, DTP)
with focus on YAML validation rules loading and field structure.
"""

import sys
import os
import yaml

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.header_segment_generator import (
    generate_transaction_purpose_code,
    generate_reference_identification,
    generate_transaction_date,
    generate_transaction_time,
    generate_time_zone_code,
    generate_additional_reference,
    generate_transaction_type_code,
    generate_action_code,
    generate_bgn_segment,
    generate_entity_identifier_code,
    generate_entity_name,
    generate_identification_code_qualifier,
    generate_identification_code,
    generate_n1_segment,
    generate_reference_identification_qualifier,
    generate_reference_identification_value,
    generate_ref_segment,
    generate_date_time_qualifier,
    generate_date_time_period_format_qualifier,
    generate_date_time_period,
    generate_dtp_segment,
    generate_header_data
)

def load_header_yaml_specs():
    """Load header segment specifications from YAML file."""
    yaml_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'header_segment_specifications.yaml')
    
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
    """Test that header YAML specifications can be loaded."""
    print("Testing header YAML specifications loading...")
    
    specs = load_header_yaml_specs()
    
    if specs is None:
        print("⚠️  Header YAML file not found or invalid - skipping YAML-based tests")
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
    
    print("✅ Header YAML specifications loaded successfully")
    return True

def test_header_segment_structure():
    """Test that header segments have correct structure."""
    print("Testing header segment structure...")
    
    # Test BGN segment
    bgn_segment = generate_bgn_segment()
    assert bgn_segment.startswith("BGN*"), f"BGN segment should start with 'BGN*', got: {bgn_segment}"
    assert bgn_segment.endswith("~"), f"BGN segment should end with '~', got: {bgn_segment}"
    
    # Test N1 segment
    n1_segment = generate_n1_segment()
    assert n1_segment.startswith("N1*"), f"N1 segment should start with 'N1*', got: {n1_segment}"
    assert n1_segment.endswith("~"), f"N1 segment should end with '~', got: {n1_segment}"
    
    # Test REF segment
    ref_segment = generate_ref_segment()
    assert ref_segment.startswith("REF*"), f"REF segment should start with 'REF*', got: {ref_segment}"
    assert ref_segment.endswith("~"), f"REF segment should end with '~', got: {ref_segment}"
    
    # Test DTP segment
    dtp_segment = generate_dtp_segment()
    assert dtp_segment.startswith("DTP*"), f"DTP segment should start with 'DTP*', got: {dtp_segment}"
    assert dtp_segment.endswith("~"), f"DTP segment should end with '~', got: {dtp_segment}"
    
    print("✅ All header segments have correct structure")

def test_bgn_field_generation():
    """Test BGN field generators."""
    print("Testing BGN field generators...")
    
    # Test BGN field generators
    purpose_code = generate_transaction_purpose_code()
    assert len(purpose_code) == 2, f"BGN01 should be 2 characters, got: {len(purpose_code)}"
    assert purpose_code.isdigit(), f"BGN01 should be numeric, got: {purpose_code}"
    
    ref_id = generate_reference_identification()
    assert len(ref_id) > 0, f"BGN02 should not be empty, got: {ref_id}"
    
    date = generate_transaction_date()
    assert len(date) == 8, f"BGN03 should be 8 characters (CCYYMMDD), got: {len(date)}"
    assert date.isdigit(), f"BGN03 should be numeric, got: {date}"
    
    time = generate_transaction_time()
    assert len(time) == 6, f"BGN04 should be 6 characters (HHMMSS), got: {len(time)}"
    assert time.isdigit(), f"BGN04 should be numeric, got: {time}"
    
    timezone = generate_time_zone_code()
    assert len(timezone) == 3, f"BGN05 should be 3 characters, got: {len(timezone)}"
    assert timezone.isalpha(), f"BGN05 should be alphabetic, got: {timezone}"
    
    action_code = generate_action_code()
    assert len(action_code) == 2, f"BGN08 should be 2 characters, got: {len(action_code)}"
    assert action_code.isdigit(), f"BGN08 should be numeric, got: {action_code}"
    
    print("✅ BGN field generators work correctly")

def test_header_data_generation():
    """Test that header data generation works correctly."""
    print("Testing header data generation...")
    
    header_data = generate_header_data()
    
    # Check that all expected segments are present
    expected_segments = ["bgn", "n1", "ref", "dtp"]
    for segment_type in expected_segments:
        assert segment_type in header_data, f"Header data should contain {segment_type}"
        assert isinstance(header_data[segment_type], list), f"{segment_type} should be a list"
        assert len(header_data[segment_type]) > 0, f"{segment_type} should not be empty"
    
    # Check that segments are valid
    for segment in header_data["bgn"]:
        assert segment.startswith("BGN*"), f"BGN segment should start with 'BGN*', got: {segment}"
    
    for segment in header_data["n1"]:
        assert segment.startswith("N1*"), f"N1 segment should start with 'N1*', got: {segment}"
    
    for segment in header_data["ref"]:
        assert segment.startswith("REF*"), f"REF segment should start with 'REF*', got: {segment}"
    
    for segment in header_data["dtp"]:
        assert segment.startswith("DTP*"), f"DTP segment should start with 'DTP*', got: {segment}"
    
    print("✅ Header data generation works correctly")

def test_yaml_validation_rules():
    """Test YAML validation rules if available."""
    print("Testing YAML validation rules...")
    
    specs = load_header_yaml_specs()
    
    if specs is None or 'validation_rules' not in specs:
        print("⚠️  Skipping YAML validation rules test - no rules available")
        return
    
    validation_rules = specs['validation_rules']
    assert isinstance(validation_rules, dict), "Validation rules should be a dictionary"
    
    # Check for common validation rule types
    rule_types = [
        'transaction_begins_with_bgn',
        'bgn_field_count',
        'n1_field_count',
        'ref_field_count',
        'dtp_field_count',
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
    
    specs = load_header_yaml_specs()
    
    if specs is None or 'fields' not in specs:
        print("⚠️  Skipping field validation rules test - no field rules available")
        return
    
    fields = specs['fields']
    assert isinstance(fields, dict), "Fields should be a dictionary"
    
    # Check for common header fields
    expected_fields = ['BGN01', 'BGN02', 'BGN03', 'BGN04', 'BGN05', 'BGN06', 'BGN07', 'BGN08', 
                      'N101', 'N102', 'N103', 'N104', 'REF01', 'REF02', 'DTP01', 'DTP02', 'DTP03']
    
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
    
    # Test header segments
    header_data = generate_header_data()
    
    for segment_type, segments in header_data.items():
        for segment in segments:
            # Extract field content (between * delimiters, excluding segment identifier)
            fields = segment.split("*")[1:]  # Skip segment identifier
            for field in fields:
                field_content = field.rstrip("~")  # Remove segment terminator
                for delimiter in edi_delimiters:
                    assert delimiter not in field_content, f"Field content contains delimiter '{delimiter}': {repr(field_content)}"
    
    print("✅ No EDI delimiters found in field content")

def test_date_format_validation():
    """Test that date formats are correct."""
    print("Testing date format validation...")
    
    # Test BGN date (CCYYMMDD format)
    bgn_date = generate_transaction_date()
    assert len(bgn_date) == 8, f"BGN date should be 8 characters (CCYYMMDD), got: {len(bgn_date)}"
    assert bgn_date.isdigit(), f"BGN date should be numeric, got: {bgn_date}"
    
    # Test BGN time (HHMMSS format)
    bgn_time = generate_transaction_time()
    assert len(bgn_time) == 6, f"BGN time should be 6 characters (HHMMSS), got: {len(bgn_time)}"
    assert bgn_time.isdigit(), f"BGN time should be numeric, got: {bgn_time}"
    
    # Test DTP date (CCYYMMDD format)
    dtp_date = generate_date_time_period()
    assert len(dtp_date) == 8, f"DTP date should be 8 characters (CCYYMMDD), got: {len(dtp_date)}"
    assert dtp_date.isdigit(), f"DTP date should be numeric, got: {dtp_date}"
    
    print("✅ Date format validation passed")

def main():
    """Run all header segment generator tests."""
    print("🧪 Testing Header Segment Generator")
    print("====================================")
    
    try:
        yaml_loaded = test_yaml_loading()
        test_header_segment_structure()
        test_bgn_field_generation()
        test_header_data_generation()
        test_date_format_validation()
        
        if yaml_loaded:
            test_yaml_validation_rules()
            test_field_validation_rules()
        
        test_edi_delimiter_safety()
        
        print("\n🎉 All header segment generator tests passed!")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
