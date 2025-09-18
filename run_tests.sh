#!/bin/bash
# Test runner for EDI 834 Trainer

echo "🧪 Running EDI 834 Trainer Tests"
echo "================================="

# Make sure we're in the project root
cd "$(dirname "$0")"

# Test segment loading
echo ""
echo "📋 Testing segment list loading..."
cd tests
python3 test_segments.py
SEGMENT_TEST_RESULT=$?
cd ..

# Test generic error generator
echo ""
echo "🔧 Testing generic error generator..."
cd tests
python3 test_generic_error_generator.py
GENERIC_ERROR_GENERATOR_TEST_RESULT=$?
cd ..

# Check results
if [ $SEGMENT_TEST_RESULT -eq 0 ] && [ $GENERIC_ERROR_GENERATOR_TEST_RESULT -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    exit 0
else
    echo ""
    echo "❌ Tests failed!"
    exit 1
fi
