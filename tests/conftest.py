"""
Pytest configuration and fixtures.

Provides common fixtures and configuration for all tests.
"""

import pytest
import sys
from pathlib import Path

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_isa_segment():
    """Provide a sample ISA segment for testing."""
    return "ISA*00*          *00*          *ZZ*SENDER_ID      *ZZ*RECEIVER_ID    *250917*1430*^00501*000000001*0*P*:~"


@pytest.fixture
def sample_iea_segment():
    """Provide a sample IEA segment for testing."""
    return "IEA*1*000000001~"


@pytest.fixture
def sample_isa_iea_pair():
    """Provide a sample ISA/IEA pair for testing."""
    return {
        "isa_segment": "ISA*00*          *00*          *ZZ*SENDER_ID      *ZZ*RECEIVER_ID    *250917*1430*^00501*000000001*0*P*:~",
        "iea_segment": "IEA*1*000000001~",
        "error_info": None,
        "shared_data": {
            "control_number": "000000001",
            "group_count": "1",
            "version": "00501",
            "date": "250917",
            "time": "1430",
            "sender_id": "SENDER_ID      ",
            "receiver_id": "RECEIVER_ID    ",
            "sender_qualifier": "ZZ",
            "receiver_qualifier": "ZZ"
        }
    }


@pytest.fixture
def sample_error_info():
    """Provide sample error info for testing."""
    return {
        "error_type": "field_error",
        "error_target": "isa_sender_qualifier",
        "field_name": "sender_qualifier",
        "segment": "ISA"
    }


@pytest.fixture
def temp_file():
    """Provide a temporary file for testing."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_file = f.name
    yield temp_file
    # Cleanup
    import os
    if os.path.exists(temp_file):
        os.unlink(temp_file)


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


# Test collection configuration
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Mark CLI tests as integration tests
        if "test_cli" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        else:
            item.add_marker(pytest.mark.unit)
        
        # Mark tests with many iterations as slow
        if any(keyword in item.name for keyword in ["many", "multiple", "distribution", "variety"]):
            item.add_marker(pytest.mark.slow)
