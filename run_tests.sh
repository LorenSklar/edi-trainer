#!/bin/bash
# Test runner for EDI 834 Trainer

echo "🧪 Running EDI 834 Trainer Tests"
echo "================================="

# Make sure we're in the project root
cd "$(dirname "$0")"

# Test envelope segment generator
echo ""
echo "🏗️ Testing envelope segment generator..."
cd tests
python3 test_envelope_segment_generator.py
ENVELOPE_GENERATOR_TEST_RESULT=$?
cd ..

# Test member segment generator
echo ""
echo "👤 Testing member segment generator..."
cd tests
python3 test_member_segment_generator.py
MEMBER_GENERATOR_TEST_RESULT=$?
cd ..

# Test coverage segment generator
echo ""
echo "🏥 Testing coverage segment generator..."
cd tests
python3 test_coverage_segment_generator.py
COVERAGE_GENERATOR_TEST_RESULT=$?
cd ..

# Check results
if [ $ENVELOPE_GENERATOR_TEST_RESULT -eq 0 ] && [ $MEMBER_GENERATOR_TEST_RESULT -eq 0 ] && [ $COVERAGE_GENERATOR_TEST_RESULT -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    exit 0
else
    echo ""
    echo "❌ Tests failed!"
    exit 1
fi
