# EDI Trainer

> Learn healthcare enrollment EDI transactions through realistic examples and interactive training

## What is this?

EDI 834 (Health Care Benefit Enrollment and Maintenance) transactions are the backbone of healthcare enrollment systems, but learning them is brutal. Most training materials are dry specifications that don't prepare you for real-world scenarios. This tool generates realistic 834 transactions with controllable error rates, matching 999 acknowledgments, and interactive learning modules.

**Perfect for:**
- **Healthcare enrollment specialists** preparing for job interviews
- **Developers** integrating with healthcare systems
- **Anyone** who needs to understand EDI without paying for expensive enterprise training

## Why does this exist?

The current EDI learning ecosystem is broken:
- **Training materials** cost thousands of dollars
- **Specifications** are unreadable for beginners
- **No realistic test data** for practice
- **Error scenarios** are poorly documented
- **Most tools** are enterprise-focused, not educational

We're building the EDI trainer we wished existed when we were learning this stuff.

## Features

### Current (v1.0)
- **Realistic 834 Generation**: Creates valid enrollment transactions using faker data
- **Controllable Error Injection**: Generate clean data or inject common errors at adjustable rates
- **Gradual Release of Responsibility (GRR)**: Toggle error explanations on/off for scaffolded learning
- **Matching Acknowledgments**: Automatic generation of correct 997/999 responses
- **Batch Processing**: Generate single transactions for learning or 1000+ for testing tools
- **Multiple Scenarios**: New hire, termination, plan changes, life events
- **Text File Output**: Standard .txt/.edi files that work with existing EDI tools

### Roadmap

## Phase 1: Core CLI Training
- **v1.0**: CLI generates ISA/IEA pairs with controllable error injection
- **v1.1**: Modular segment generators (ISA generator, IEA generator, etc)
- **v1.2**: Modular field generators including with_error parameter
- **v1.3**: Generic error generators
- **v1.4**: YAML-driven clean field generation
- **v1.5**: YAML-driven error field generation with error explanations embedded so full specifications for each field is available

## Phase 2: Complete 834 Segments
- **v2.0**: CLI generates a full 834 transaction (ISA + GS + ST → segments → SE + GE + IEA)
- **v2.1**: Add header segments (BGN, REF, DTP)
- **v2.2**: Member demographic loop (INS, NM1, PER)
- **v2.3**: Member coverage loop (HD, DTP, REF)
- **v2.4**: Benefit election loop (BEN, AMT, COB)
- **v2.5**: CLI generates 997/999 acknowledgments in response to the 834 with and without errors

## Phase 3: Add Multiple Choice
- **v3.0**: REST API (single record or bulk generation)
- **v3.1**: Svelte frontend for transaction viewer
- **v3.2**: Question types include:
    - Identify correct segment given a field
    - Identify correct field given segment
    - Identify the field with the error
    - Correct field with error
    - Identify structural error
    - Correct structural error
## Phase 4: Full constructivist tool
- **v4.0**: NLP answers with AI feedback
- **v4.1**: Scaffolding learning modules with progressive difficulty
- **v4.2**: Enrichment activities for advanced learners
- **v4.3**: Non-linear learning paths based on individual progress

**Why this approach?**
- Each version is shippable and provides immediate value
- Validates core assumptions before adding complexity
- Follows GRR (Gradual Release of Responsibility) pedagogy

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate a single transaction with guaranteed errors
python edi_trainer.py --error-rate=1.0

# Generate a single transaction with realistic error rate
python edi_trainer.py -e 0.3

# Skip interactive mode and show errors immediately
python edi_trainer.py -e 0.3 -d
```

## Common Use Cases

### Enrollment Specialist Job Training
```bash
# Step 1: Guaranteed errors and see error report immediately
python edi_trainer.py --count=5 --error-rate=1.0 --display-error

# Step 2: Guaranteed errors and identify error before checking
python edi_trainer.py --count=5 --error-rate=1.0

# Step 3: Realistic mix of errors and no errors
python edi_trainer.py --count=10 --error-rate=0.3
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
- `--display-error`: Show error report immediately (disables learning mode)
- `--learning-mode`: Interactive mode - wait for user input before showing errors (default)

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
