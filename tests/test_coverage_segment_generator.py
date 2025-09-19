#!/usr/bin/env python3
"""
Test Coverage Segment Generator

Tests the generation of coverage segments (N1, INS, REF, DTP, HD, COB)
with focus on YAML validation rules loading and field structure.
"""

import sys
import os
import yaml

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.coverage_segment_generator import (
    generate_n1_segment,
    generate_ins_segment,
    generate_ref_segment,
    generate_dtp_segment,
    generate_hd_segment,
    generate_cob_segment,
    generate_coverage_data
)

def load_coverage_yaml_specs():
    """Load coverage segment specifications from YAML file."""
    yaml_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'coverage_segment_specifications.yaml')
    
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
    """Test that coverage YAML specifications can be loaded."""
    print("Testing coverage YAML specifications loading...")
    
    specs = load_coverage_yaml_specs()
    
    if specs is None:
        print("⚠️  Coverage YAML file not found or invalid - skipping YAML-based tests")
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
    
    print("✅ Coverage YAML specifications loaded successfully")
    return True

def test_coverage_segment_structure():
    """Test that coverage segments have correct structure."""
    print("Testing coverage segment structure...")
    
    # Test N1 segment
    n1_segment = generate_n1_segment()
    assert n1_segment.startswith("N1*"), f"N1 segment should start with 'N1*', got: {n1_segment}"
    assert n1_segment.endswith("~"), f"N1 segment should end with '~', got: {n1_segment}"
    
    # Test INS segment
    ins_segment = generate_ins_segment()
    assert ins_segment.startswith("INS*"), f"INS segment should start with 'INS*', got: {ins_segment}"
    assert ins_segment.endswith("~"), f"INS segment should end with '~', got: {ins_segment}"
    
    # Test REF segment
    ref_segment = generate_ref_segment()
    assert ref_segment.startswith("REF*"), f"REF segment should start with 'REF*', got: {ref_segment}"
    assert ref_segment.endswith("~"), f"REF segment should end with '~', got: {ref_segment}"
    
    # Test DTP segment
    dtp_segment = generate_dtp_segment()
    assert dtp_segment.startswith("DTP*"), f"DTP segment should start with 'DTP*', got: {dtp_segment}"
    assert dtp_segment.endswith("~"), f"DTP segment should end with '~', got: {dtp_segment}"
    
    # Test HD segment
    hd_segment = generate_hd_segment()
    assert hd_segment.startswith("HD*"), f"HD segment should start with 'HD*', got: {hd_segment}"
    assert hd_segment.endswith("~"), f"HD segment should end with '~', got: {hd_segment}"
    
    # Test COB segment
    cob_segment = generate_cob_segment()
    assert cob_segment.startswith("COB*"), f"COB segment should start with 'COB*', got: {cob_segment}"
    assert cob_segment.endswith("~"), f"COB segment should end with '~', got: {cob_segment}"
    
    print("✅ All coverage segments have correct structure")

def test_coverage_data_generation():
    """Test that coverage data generation works correctly."""
    print("Testing coverage data generation...")
    
    coverage_data = generate_coverage_data()
    
    # Check that all expected segments are present
    expected_segments = ["n1_segments", "ins", "ref_segments", "dtp_segments", "hd_segments", "cob"]
    for segment_type in expected_segments:
        assert segment_type in coverage_data, f"Coverage data should contain {segment_type}"
        assert isinstance(coverage_data[segment_type], list), f"{segment_type} should be a list"
        assert len(coverage_data[segment_type]) > 0, f"{segment_type} should not be empty"
    
    # Check that segments are valid
    for segment in coverage_data["n1_segments"]:
        assert segment.startswith("N1*"), f"N1 segment should start with 'N1*', got: {segment}"
    
    for segment in coverage_data["ins"]:
        assert segment.startswith("INS*"), f"INS segment should start with 'INS*', got: {segment}"
    
    for segment in coverage_data["ref_segments"]:
        assert segment.startswith("REF*"), f"REF segment should start with 'REF*', got: {segment}"
    
    for segment in coverage_data["dtp_segments"]:
        assert segment.startswith("DTP*"), f"DTP segment should start with 'DTP*', got: {segment}"
    
    for segment in coverage_data["hd_segments"]:
        assert segment.startswith("HD*"), f"HD segment should start with 'HD*', got: {segment}"
    
    for segment in coverage_data["cob"]:
        assert segment.startswith("COB*"), f"COB segment should start with 'COB*', got: {segment}"
    
    print("✅ Coverage data generation works correctly")

def test_yaml_validation_rules():
    """Test YAML validation rules if available."""
    print("Testing YAML validation rules...")
    
    specs = load_coverage_yaml_specs()
    
    if specs is None or 'validation_rules' not in specs:
        print("⚠️  Skipping YAML validation rules test - no rules available")
        return
    
    validation_rules = specs['validation_rules']
    assert isinstance(validation_rules, dict), "Validation rules should be a dictionary"
    
    # Check for common validation rule types
    rule_types = [
        'transaction_begins_with_n1',
        'n1_field_count',
        'ins_field_count',
        'ref_field_count',
        'dtp_field_count',
        'hd_field_count',
        'cob_field_count',
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
    
    specs = load_coverage_yaml_specs()
    
    if specs is None or 'fields' not in specs:
        print("⚠️  Skipping field validation rules test - no field rules available")
        return
    
    fields = specs['fields']
    assert isinstance(fields, dict), "Fields should be a dictionary"
    
    # Check for common coverage fields
    expected_fields = ['N101', 'N102', 'INS01', 'INS02', 'INS03', 'REF01', 'REF02', 'DTP01', 'DTP02', 'DTP03', 'HD01', 'HD03', 'HD04', 'COB01', 'COB02', 'COB03']
    
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
    
    # Test coverage segments
    coverage_data = generate_coverage_data()
    
    for segment_type, segments in coverage_data.items():
        for segment in segments:
            # Extract field content (between * delimiters, excluding segment identifier)
            fields = segment.split("*")[1:]  # Skip segment identifier
            for field in fields:
                field_content = field.rstrip("~")  # Remove segment terminator
                for delimiter in edi_delimiters:
                    assert delimiter not in field_content, f"Field content contains delimiter '{delimiter}': {repr(field_content)}"
    
    print("✅ No EDI delimiters found in field content")

def test_purpose_specific_generation():
    """Test purpose-specific segment generation."""
    print("Testing purpose-specific segment generation...")
    
    from core.coverage_segment_generator import (
        generate_n1_segment_with_purpose,
        generate_ref_segment_with_purpose,
        generate_dtp_segment_with_purpose,
        generate_hd_segment_with_purpose
    )
    
    # Test N1 segment with different purposes
    sponsor_n1 = generate_n1_segment_with_purpose("sponsor", {})
    insurance_n1 = generate_n1_segment_with_purpose("insurance_company", {})
    broker_n1 = generate_n1_segment_with_purpose("broker", {})
    
    assert sponsor_n1.startswith("N1*P5*"), f"Sponsor N1 should start with 'N1*P5*', got: {sponsor_n1}"
    assert insurance_n1.startswith("N1*IN*"), f"Insurance N1 should start with 'N1*IN*', got: {insurance_n1}"
    assert broker_n1.startswith("N1*BO*"), f"Broker N1 should start with 'N1*BO*', got: {broker_n1}"
    
    # Test REF segment with different purposes
    subscriber_ref = generate_ref_segment_with_purpose("subscriber_id", {})
    group_ref = generate_ref_segment_with_purpose("group_number", {})
    policy_ref = generate_ref_segment_with_purpose("policy_number", {})
    
    assert subscriber_ref.startswith("REF*0F*"), f"Subscriber REF should start with 'REF*0F*', got: {subscriber_ref}"
    assert group_ref.startswith("REF*1L*"), f"Group REF should start with 'REF*1L*', got: {group_ref}"
    assert policy_ref.startswith("REF*CE*"), f"Policy REF should start with 'REF*CE*', got: {policy_ref}"
    
    # Test DTP segment with different purposes
    eligibility_dtp = generate_dtp_segment_with_purpose("eligibility_date", {})
    coverage_begin_dtp = generate_dtp_segment_with_purpose("coverage_begin", {})
    
    assert eligibility_dtp.startswith("DTP*356*"), f"Eligibility DTP should start with 'DTP*356*', got: {eligibility_dtp}"
    assert coverage_begin_dtp.startswith("DTP*348*"), f"Coverage begin DTP should start with 'DTP*348*', got: {coverage_begin_dtp}"
    
    # Test HD segment with different purposes
    health_hd = generate_hd_segment_with_purpose("health", {})
    dental_hd = generate_hd_segment_with_purpose("dental", {})
    vision_hd = generate_hd_segment_with_purpose("vision", {})
    
    assert health_hd.startswith("HD*030*"), f"Health HD should start with 'HD*030*', got: {health_hd}"
    assert dental_hd.startswith("HD*DENT*"), f"Dental HD should start with 'HD*DENT*', got: {dental_hd}"
    assert vision_hd.startswith("HD*VIS*"), f"Vision HD should start with 'HD*VIS*', got: {vision_hd}"
    
    print("✅ Purpose-specific segment generation works correctly")

def main():
    """Run all coverage segment generator tests."""
    print("🧪 Testing Coverage Segment Generator")
    print("=====================================")
    
    try:
        yaml_loaded = test_yaml_loading()
        test_coverage_segment_structure()
        test_coverage_data_generation()
        test_purpose_specific_generation()
        
        if yaml_loaded:
            test_yaml_validation_rules()
            test_field_validation_rules()
        
        test_edi_delimiter_safety()
        
        print("\n🎉 All coverage segment generator tests passed!")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
