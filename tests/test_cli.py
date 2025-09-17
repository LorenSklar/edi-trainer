"""
Tests for CLI interface.

Tests the edi_trainer.py command-line interface functionality.

TODO - OUTSTANDING TEST FAILURES:
1. CLI help text still references "EDI 834" instead of "EDI Trainer"
2. test_cli_error_rate_parameter expects 10 ISA* but gets 8 (some transactions have errors)
3. test_cli_explain_errors fails due to get_error_explanation function signature mismatch
4. test_cli_isa_segment_format expects 17 fields but gets 16 (missing component separator)
5. test_cli_iea_segment_format expects numeric control number but gets control number with ~ terminator
6. test_cli_generates_different_data expects unique control numbers but gets duplicates
"""

import pytest
import subprocess
import sys
import tempfile
import os
from pathlib import Path


class TestCLIBasicFunctionality:
    """Test basic CLI functionality."""
    
    def test_cli_help(self):
        """Test that CLI shows help when requested."""
        result = subprocess.run(
            [sys.executable, "edi_trainer.py", "--help"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "Generate EDI 834 transactions" in result.stdout
        assert "--count" in result.stdout
        assert "--error-rate" in result.stdout
        assert "--explain-errors" in result.stdout
    
    def test_cli_default_behavior(self):
        """Test CLI default behavior (no arguments)."""
        result = subprocess.run(
            [sys.executable, "edi_trainer.py"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "ISA*" in result.stdout
        assert "IEA*" in result.stdout
        assert result.stdout.count("ISA*") == 1  # Should generate 1 pair by default
        assert result.stdout.count("IEA*") == 1
    
    def test_cli_count_parameter(self):
        """Test CLI count parameter."""
        result = subprocess.run(
            [sys.executable, "edi_trainer.py", "--count=3"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert result.stdout.count("ISA*") == 3
        assert result.stdout.count("IEA*") == 3
    
    def test_cli_error_rate_parameter(self):
        """Test CLI error rate parameter."""
        # Test with 100% error rate to ensure we get errors
        result = subprocess.run(
            [sys.executable, "edi_trainer.py", "--count=10", "--error-rate=1.0"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        # Should still generate segments (even if they have errors)
        assert result.stdout.count("ISA*") == 10
        assert result.stdout.count("IEA*") == 10
    
    def test_cli_output_to_file(self):
        """Test CLI output to file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            temp_file = f.name
        
        try:
            result = subprocess.run(
                [sys.executable, "edi_trainer.py", "--count=2", "--output", temp_file],
                capture_output=True,
                text=True
            )
            
            assert result.returncode == 0
            assert f"Generated 2 ISA/IEA pairs to {temp_file}" in result.stdout
            
            # Check file was created and has content
            assert os.path.exists(temp_file)
            with open(temp_file, 'r') as f:
                content = f.read()
                assert "ISA*" in content
                assert "IEA*" in content
                assert content.count("ISA*") == 2
                assert content.count("IEA*") == 2
        
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_cli_verbose_mode(self):
        """Test CLI verbose mode."""
        result = subprocess.run(
            [sys.executable, "edi_trainer.py", "--count=1", "--verbose"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "# Transaction 1/1" in result.stdout
        assert "# End Transaction" in result.stdout
    
    def test_cli_explain_errors(self):
        """Test CLI explain errors mode."""
        result = subprocess.run(
            [sys.executable, "edi_trainer.py", "--count=1", "--error-rate=1.0", "--explain-errors"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        # Should have error explanation (though it might be empty if no errors generated)
        assert "ISA*" in result.stdout
        assert "IEA*" in result.stdout


class TestCLIErrorHandling:
    """Test CLI error handling."""
    
    def test_cli_invalid_error_rate(self):
        """Test CLI with invalid error rate."""
        result = subprocess.run(
            [sys.executable, "edi_trainer.py", "--error-rate=1.5"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        assert "error-rate must be between 0.0 and 1.0" in result.stderr
    
    def test_cli_negative_error_rate(self):
        """Test CLI with negative error rate."""
        result = subprocess.run(
            [sys.executable, "edi_trainer.py", "--error-rate=-0.1"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        assert "error-rate must be between 0.0 and 1.0" in result.stderr
    
    def test_cli_invalid_count(self):
        """Test CLI with invalid count."""
        result = subprocess.run(
            [sys.executable, "edi_trainer.py", "--count=0"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        assert "count must be at least 1" in result.stderr
    
    def test_cli_negative_count(self):
        """Test CLI with negative count."""
        result = subprocess.run(
            [sys.executable, "edi_trainer.py", "--count=-1"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode != 0
        assert "count must be at least 1" in result.stderr


class TestCLIOutputFormat:
    """Test CLI output format."""
    
    def test_cli_output_structure(self):
        """Test that CLI output has proper structure."""
        result = subprocess.run(
            [sys.executable, "edi_trainer.py", "--count=2"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        
        # Should have ISA and IEA segments
        isa_lines = [line for line in lines if line.startswith("ISA*")]
        iea_lines = [line for line in lines if line.startswith("IEA*")]
        
        assert len(isa_lines) == 2
        assert len(iea_lines) == 2
        
        # Each segment should end with ~
        for line in isa_lines + iea_lines:
            assert line.endswith("~")
    
    def test_cli_isa_segment_format(self):
        """Test ISA segment format."""
        result = subprocess.run(
            [sys.executable, "edi_trainer.py", "--count=1"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        isa_line = next(line for line in lines if line.startswith("ISA*"))
        
        # ISA should have correct number of fields
        parts = isa_line.split("*")
        assert len(parts) == 17  # 16 fields + segment identifier
        
        # Check specific field positions
        assert parts[0] == "ISA"
        assert parts[1] == "00"  # Auth qualifier
        assert parts[3] == "00"  # Security qualifier
        assert parts[5] == "ZZ"  # Sender qualifier (default)
        assert parts[7] == "ZZ"  # Receiver qualifier (default)
        assert parts[12] == "00501"  # Version (default)
        assert parts[14] == "0"  # Acknowledgment (default)
        assert parts[15] == "P"  # Usage indicator (default)
    
    def test_cli_iea_segment_format(self):
        """Test IEA segment format."""
        result = subprocess.run(
            [sys.executable, "edi_trainer.py", "--count=1"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        iea_line = next(line for line in lines if line.startswith("IEA*"))
        
        # IEA should have correct number of fields
        parts = iea_line.split("*")
        assert len(parts) == 3  # 2 fields + segment identifier
        
        # Check specific field positions
        assert parts[0] == "IEA"
        assert parts[1].isdigit()  # Group count should be numeric
        assert parts[2].isdigit()  # Control number should be numeric


class TestCLIIntegration:
    """Test CLI integration with core modules."""
    
    def test_cli_imports_work(self):
        """Test that CLI can import all required modules."""
        result = subprocess.run(
            [sys.executable, "-c", "import sys; sys.path.insert(0, 'src'); from core.segment_generators import generate_isa_iea_pair; print('Import successful')"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "Import successful" in result.stdout
    
    def test_cli_generates_different_data(self):
        """Test that CLI generates different data on multiple runs."""
        results = []
        
        # Run CLI multiple times
        for _ in range(3):
            result = subprocess.run(
                [sys.executable, "edi_trainer.py", "--count=1"],
                capture_output=True,
                text=True
            )
            assert result.returncode == 0
            results.append(result.stdout)
        
        # Should have different control numbers
        control_numbers = []
        for output in results:
            lines = output.strip().split('\n')
            isa_line = next(line for line in lines if line.startswith("ISA*"))
            parts = isa_line.split("*")
            control_numbers.append(parts[13])  # ISA13 is control number
        
        # Should have different control numbers
        assert len(set(control_numbers)) > 1
