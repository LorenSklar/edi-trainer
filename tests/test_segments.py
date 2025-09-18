#!/usr/bin/env python3
"""
Test script to verify segment list loading from YAML files.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.transaction_generator import load_segment_list


def test_segment_loading():
    """Test that segment list is properly loaded from YAML files."""
    print("Testing segment list loading...")
    
    segments = load_segment_list(verbose=True)
    
    print(f"Found {len(segments)} segments: {segments}")

    
    # Test that we don't have empty segments
    assert len(segments) > 0, "No segments loaded"
    
    # Test that segments are strings
    for segment in segments:
        assert isinstance(segment, str), f"Segment {segment} is not a string"
    
    return True


if __name__ == "__main__":
    try:
        test_segment_loading()
        print("\n🎉 All segement tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Segment test failed: {e}")
        sys.exit(1)
