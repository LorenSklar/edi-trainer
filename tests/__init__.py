"""
EDI 834 Trainer Test Suite

This package contains comprehensive tests for the EDI 834 Trainer system.

Test modules:
- test_field_generators.py: Tests for individual field generation
- test_segment_generators.py: Tests for ISA/IEA pair generation
- test_cli.py: Tests for command-line interface
- conftest.py: Pytest configuration and fixtures

Run tests with:
    pytest tests/
    pytest tests/ -v  # verbose output
    pytest tests/ -m "not slow"  # skip slow tests
    pytest tests/test_field_generators.py  # run specific test file
"""
