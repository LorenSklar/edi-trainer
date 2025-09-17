# EDI 834 Trainer

> Learn healthcare enrollment EDI transactions through realistic examples and interactive training

## What is this?

EDI 834 (Health Care Benefit Enrollment and Maintenance) transactions are the backbone of healthcare enrollment systems, but learning them is brutal. Most training materials are dry specifications that don't prepare you for real-world scenarios. This tool generates realistic 834 transactions with controllable error rates, matching 999 acknowledgments, and interactive learning modules.

**Perfect for:**
- Healthcare enrollment specialists preparing for job interviews
- Developers integrating with healthcare systems
- Anyone who needs to understand EDI without paying for expensive enterprise training

## Why does this exist?

The current EDI learning ecosystem is broken:
- Training materials cost thousands of dollars
- Specifications are unreadable for beginners
- No realistic test data for practice
- Error scenarios are poorly documented
- Most tools are enterprise-focused, not educational

We're building the EDI trainer we wished existed when we were learning this stuff.

## Features

### Current (v1.0)
- **Realistic 834 Generation**: Creates valid enrollment transactions using faker data
- **Controllable Error Injection**: Generate clean data or inject common errors at adjustable rates
- **Gradual Release of Responsibility (GRR)**: Toggle error explanations on/off for scaffolded learning
- **Matching 999 Responses**: Automatic generation of correct acknowledgments for any 834
- **Batch Processing**: Generate single transactions for learning or 1000+ for testing tools
- **Multiple Scenarios**: New hire, termination, plan changes, life events
- **Text File Output**: Standard .txt/.edi files that work with existing EDI tools

### Roadmap (Deep, Then Broad)

We're building this tool incrementally, going deep on core functionality before expanding to other EDI segments:

**Phase 1: Deep on 834 (v1.0 - v6.0)**
- **v1.0**: CLI with ISA/IEA pair generation and error injection
- **v2.0**: CLI with full 834 segments + comprehensive error explanations  
- **v3.0**: REST API for programmatic access and integration testing
- **v4.0**: Svelte frontend with transaction viewer and interactive learning
- **v5.0**: Interactive learning modules (flashcards, multiple choice, quizzes)
- **v6.0**: Progress tracking and adaptive learning algorithms

**Phase 2: Broad to Other Segments (v7.0+)**
- **v7.0**: AI-powered tutor with natural language feedback and personalized learning paths
- **v8.0**: EDI 997/999 (Functional/Implementation Acknowledgments) training
- **v9.0**: EDI 835 (Payment/Remittance) transaction training
- **v10.0**: EDI 837 (Claims) transaction training  
- **v11.0**: EDI 270/271 (Eligibility) transaction training
- **v12.0**: Cross-transaction workflows and end-to-end scenarios
- **v13.0**: Carrier-specific companion guide training modules

**Why this approach?**
- Each version is shippable and provides immediate value
- Validates core assumptions before adding complexity
- Follows GRR (Gradual Release of Responsibility) pedagogy
- Minimizes technical debt and maximizes learning effectiveness
- Deep expertise on 834 before expanding to other segments

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate 10 clean 834 transactions
python edi_trainer.py --count=10 --error-rate=0.0 --output=clean_batch.txt

# Generate 100 transactions with 15% error rate (no explanations)
python edi_trainer.py --count=100 --error-rate=0.15 --output=test_batch.txt

# Generate single transaction for learning with error explanations
python edi_trainer.py --count=1 --scenario=new_hire --error-rate=0.3 --explain-errors --output=learning.txt
```

## Common Use Cases

### Job Interview Prep (GRR Learning Approach)
```bash
# Step 1: Practice identifying errors without help
python edi_trainer.py --count=5 --scenario=new_hire --error-rate=0.2 --output=challenge.txt

# Step 2: Get explanations to reinforce learning
python edi_trainer.py --count=5 --scenario=new_hire --error-rate=0.2 --explain-errors --output=learning.txt

# Step 3: Test yourself again without explanations
python edi_trainer.py --count=10 --error-rate=0.3 --output=final_test.txt
```

### System Testing
```bash
# Generate large batches for load testing
python edi_trainer.py --count=1000 --error-rate=0.05 --format=batch --output=load_test.txt

# Create edge cases for error handling
python edi_trainer.py --count=50 --error-rate=0.5 --output=edge_cases.txt
```

### Learning EDI Structure
```bash
# Single clean transaction to study
python edi_trainer.py --count=1 --verbose --output=study.txt

# Practice with guided error explanations
python edi_trainer.py --count=3 --error-rate=0.4 --explain-errors --verbose --output=guided_learning.txt
```

## Understanding the Output

### 834 Transaction Structure
```
ISA*00*          *00*          *ZZ*SENDER         *ZZ*RECEIVER       *250917*1430*^*00501*000000001*0*P*:~
GS*BE*SENDERGS*RECEIVERGS*20250917*1430*1*X*005010X220A1~
ST*834*0001*005010X220A1~
BGN*00*12345*20250917*143000****4~
N1*P5*ACME CORPORATION*FI*123456789~
INS*Y*18*001***FT~
REF*0F*987654321~
REF*1L*E001~
DTP*356*D8*20250917~
NM1*IL*1*DOE*JOHN*M***34*987654321~
DMG*D8*19900115*M~
HD*021**HLT*PLAN001~
DTP*348*D8*20250917~
SE*13*0001~
GE*1*1~
IEA*1*000000001~
```

### 999 Acknowledgment
```
ISA*00*          *00*          *ZZ*RECEIVER       *ZZ*SENDER         *250917*1435*^*00501*000000002*0*P*:~
GS*FA*RECEIVERGS*SENDERGS*20250917*1435*2*X*005010~
ST*999*0002*005010~
AK1*BE*1*005010X220A1~
AK2*834*0001*005010X220A1~
AK5*A~
AK9*A*1*1*1~
SE*7*0002~
GE*1*2~
IEA*1*000000002~
```

## Error Types with GRR Explanations

The trainer injects realistic errors you'll encounter in production. Use `--explain-errors` to get detailed explanations:

### Missing Required Segments
**Error**: Missing INS segment
**Explanation**: The INS (Insured) segment is required for all 834 transactions. It identifies the person being enrolled and their relationship to the subscriber. Without this segment, the carrier cannot process the enrollment.

### Invalid Date Formats
**Error**: DTP*356*D8*20250917 (should be CCYYMMDD format)
**Explanation**: EDI dates must be in CCYYMMDD format (8 digits). The D8 qualifier indicates this is a date, but the format must be exactly 8 digits with no separators.

### Incorrect Maintenance Type Codes
**Error**: INS*Y*99*001***FT (invalid INS02 value)
**Explanation**: INS02 (Maintenance Type Code) must be a valid value like 18 (Add), 19 (Change), or 20 (Delete). Code 99 is not a valid maintenance type and will cause the transaction to reject.

### Malformed SSNs and Member IDs
**Error**: REF*0F*123-45-6789 (SSN with dashes)
**Explanation**: EDI transactions require SSNs without formatting. Remove all dashes, spaces, and other separators. The SSN should be exactly 9 digits.

### Missing Segment Terminators
**Error**: NM1*IL*1*DOE*JOHN*M***34*987654321 (missing ~)
**Explanation**: Every EDI segment must end with a tilde (~) character. This is the segment terminator that tells the parser where one segment ends and the next begins.

### Invalid Relationship Codes
**Error**: INS*Y*18*999***FT (invalid relationship code)
**Explanation**: Relationship codes must be valid values like 001 (Spouse), 002 (Child), or 034 (Self). Code 999 is not a recognized relationship and will cause enrollment rejection.

### Date Logic Errors
**Error**: DTP*348*D8*20200101 (effective date in the past)
**Explanation**: Coverage effective dates cannot be in the past. The DTP*348 segment indicates the coverage begin date, which must be today's date or in the future.

## Configuration Options

### Enrollment Scenarios
- `new_hire`: Clean enrollment for new employee
- `termination`: Coverage ending scenarios  
- `plan_change`: Mid-year plan modifications
- `life_event`: Marriage, divorce, birth scenarios
- `cobra`: Continuation coverage
- `mixed`: Random combination of scenarios

### Error Injection & Learning
- `--error-rate 0.0`: Clean data only
- `--error-rate 0.1`: 10% of transactions have errors
- `--error-rate 0.5`: High error rate for stress testing
- `--explain-errors`: Include detailed error explanations (GRR learning)
- `--no-explain-errors`: Generate errors without explanations (challenge mode)

### Output Formats
- `single`: Individual 834 transactions
- `batch`: Multiple 834s wrapped in ISA/GS envelopes
- `verbose`: Include human-readable comments

## Contributing

This started as a personal learning tool but has grown into something the whole EDI community can use. Contributions welcome!

### Roadmap Priorities
1. More realistic error scenarios based on real production issues
2. State-specific variations (Medicaid requirements)  
3. Carrier-specific companion guides
4. Web interface for non-technical users
5. API endpoints for integration testing
6. Interactive learning modules with GRR scaffolding
7. AI-powered explanations and feedback

### Getting Started
```bash
git clone https://github.com/yourusername/edi-834-trainer
cd edi-834-trainer
pip install -r requirements.txt
python -m pytest tests/
```

## Why EDI is Hard

EDI 834 transactions were designed in the 1970s for telegraph transmission. They're positional, brittle, and break if you add a single character in the wrong place. Every carrier has different requirements despite using the "same" standard. 

This tool exists because learning EDI shouldn't require a $5,000 training course or months of trial-and-error debugging production systems.

## License

**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

**You are free to:**
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

**Under the following terms:**
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **NonCommercial** — You may not use the material for commercial purposes.

**No additional restrictions** — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.
