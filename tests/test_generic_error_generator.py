#!/usr/bin/env python3
"""
Test script for generic error generator functionality.
Tests generic field error generation with various scenarios.
"""

import sys
import os
import random

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.error_generator import field_error_generator


def test_generic_error_generation():
    """Test generic field error generation."""
    print("🧪 Testing Generic Error Generation")
    print("=" * 40)
    
    # Test field specification
    field_spec = {
        'characterset': 'numeric',
        'min_length': 3,
        'max_length': 5,
        'field_type': 'generic',
        'common_errors': ['ABC', 'XYZ'],
        'valid_values': ['123', '456', '789']
    }
    
    valid_string = "12345"
    test_count = 20
    
    print(f"Testing with valid string: '{valid_string}'")
    print(f"Field spec: {field_spec['characterset']} characters, length {field_spec['min_length']}-{field_spec['max_length']}")
    print(f"Running {test_count} tests...")
    print()
    
    error_counts = {}
    
    for i in range(test_count):
        result = field_error_generator('ISA01', field_spec, valid_string)
        error_type = result['error_type']
        error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        print(f"Test {i+1:2d}: {error_type:15} = '{result['error_value']}'")
        if error_type == 'invalid_character':
            print(f"         Explanation: {result['error_explanation']}")
    
    print()
    print("Error Type Distribution:")
    for error_type, count in sorted(error_counts.items()):
        percentage = (count / test_count) * 100
        print(f"  {error_type:15}: {count:2d} ({percentage:5.1f}%)")
    
    return True


def test_character_set_errors():
    """Test different character set error generation."""
    print("\n🔤 Testing Character Set Errors")
    print("=" * 40)
    
    character_sets = ['numeric', 'alpha', 'alphanumeric', 'printable', 'extended']
    
    for charset in character_sets:
        field_spec = {
            'characterset': charset,
            'min_length': 3,
            'max_length': 5,
            'field_type': 'generic'
        }
        
        # Generate a valid string for this character set
        from core.error_generator import generate_random_value
        valid_string = generate_random_value(charset, 4)
        
        print(f"\n{charset.upper()} character set:")
        print(f"  Valid string: '{valid_string}'")
        
        # Test invalid_character error specifically
        for i in range(3):
            result = field_error_generator('TEST01', field_spec, valid_string)
            if result['error_type'] == 'invalid_character':
                print(f"  Invalid char: '{result['error_value']}' - {result['error_explanation']}")
                break
        else:
            print(f"  No invalid_character errors generated in 3 attempts")
    
    return True


def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n⚠️  Testing Edge Cases")
    print("=" * 40)
    
    # Test with minimal field spec
    minimal_spec = {
        'characterset': 'numeric',
        'field_type': 'generic'
    }
    
    print("Minimal field spec test:")
    result = field_error_generator('MIN01', minimal_spec, '123')
    print(f"  Result: {result['error_type']} = '{result['error_value']}'")
    
    # Test with extended character set (should fallback to missing_value for invalid_character)
    extended_spec = {
        'characterset': 'extended',
        'min_length': 3,
        'max_length': 5,
        'field_type': 'generic'
    }
    
    print("\nExtended character set test:")
    for i in range(5):
        result = field_error_generator('EXT01', extended_spec, 'Hello')
        if result['error_type'] == 'invalid_character':
            print(f"  Invalid char: '{result['error_value']}' - {result['error_explanation']}")
            break
    else:
        print("  Extended character set correctly falls back to missing_value for invalid_character")
    
    return True


def main():
    """Run all error generator tests."""
    print("🧪 EDI 834 Trainer - Generic Error Generator Tests")
    print("=" * 50)
    
    try:
        # Set seed for reproducible tests
        random.seed(42)
        
        # Run tests
        test_generic_error_generation()
        test_character_set_errors()
        test_edge_cases()
        
        print("\n✅ All generic error generator tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Generic error generator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
