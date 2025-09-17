#!/bin/bash

# EDI Trainer - Test Runner
# Run all tests for the EDI Trainer system

echo "🧪 Running EDI Trainer Tests..."
echo "================================="

# Check if we're in the right directory
if [ ! -f "edi_trainer.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ Error: pytest is not installed. Please install it with:"
    echo "  pip install pytest"
    exit 1
fi

# Add src to Python path so imports work
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Run tests with different options based on arguments
if [ "$1" = "--fast" ]; then
    echo "⚡ Running fast tests (skipping slow tests)..."
    python3 -m pytest tests/ -m "not slow" -v
elif [ "$1" = "--unit" ]; then
    echo "🔧 Running unit tests only..."
    python3 -m pytest tests/ -m "unit" -v
elif [ "$1" = "--integration" ]; then
    echo "🔗 Running integration tests only..."
    python3 -m pytest tests/ -m "integration" -v
elif [ "$1" = "--coverage" ]; then
    echo "📊 Running tests with coverage..."
    if command -v coverage &> /dev/null; then
        python3 -m coverage run -m pytest tests/
        coverage report
        coverage html
        echo "📈 Coverage report generated in htmlcov/"
    else
        echo "❌ Error: coverage is not installed. Please install it with:"
        echo "  pip install coverage"
        exit 1
    fi
else
    echo "🚀 Running all tests..."
    python3 -m pytest tests/ -v
fi

echo ""
echo "✅ Test run complete!"
