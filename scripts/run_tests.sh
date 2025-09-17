#!/bin/bash

# EDI Trainer Test Runner
# Runs all tests with proper Python path setup

echo "🧪 Running EDI Trainer Tests..."

# Add src to Python path so imports work
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Run tests with verbose output
python -m pytest tests/ -v

echo "✅ Tests completed!"
