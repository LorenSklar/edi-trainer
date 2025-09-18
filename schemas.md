# EDI 834 Trainer - Data Schemas

This document defines the data structures and schemas used throughout the EDI 834 Trainer system.

## Transaction Generator Return Schema

The `generate_834_transaction()` function returns a dictionary with the following structure:

```python
{
    "transaction": str,      # Complete EDI 834 transaction string
    "error_info": dict       # Error details for GRR explanations
}
```

### Example Return Value

```python
{
    "transaction": "ISA*00*          *00*          *ZZ*SENDER_ID      *ZZ*RECEIVER_ID    *250917*1430*^*00501*000000001*0*T*:~\\nGS*BE*SENDER*RECEIVER*20250917*1430*1*X*005010X220A1~\\nST*834*0001*005010X220A1~\\n...",
    "error_info": {
        "error_target": None,
        "error_type": None,
        "error_segment": None,
        "error_field": None,
        "error_explanation": None
    }
}
```

## Error Info Schema

When errors are injected, the `error_info` dictionary contains:

```python
{
    "error_target": str,         # "segment" or "field" - where the error occurs
    "error_type": str,           # "invalid_value", "missing_value", "control_number_mismatch", etc.
    "error_segment": str|None,   # Which segment (ISA, N1, etc.) or None
    "error_field": str|None,     # Which field (ISA01, ISA06, etc.) or None
    "error_explanation": str     # Specific error description
}
```

### Error Types

**Field Errors (80% weight):**
- `blank_value` - Required field contains only spaces (correct length)
- `missing_value` - Required field is completely absent (empty string)
- `invalid_value` - Invalid field value (uses common_errors or generates random valid-format value not in valid_values)
  - **Logic**: 1) Use `common_errors` if present, 2) Generate invalid value if `valid_values` present, 3) Fallback to "N/A"
  - **Protection**: Falls back to "N/A" if neither common_errors nor valid_values present
- `invalid_character` - Includes an invalid character
- `wrong_format` - Field format is incorrect (e.g., '20250101' instead of '250101')
- `wrong_length` - Field length is incorrect

**Structural Errors (20% weight):**
- `control_number_mismatch` - ISA13 and IEA02 control numbers don't match
- `date_time_mismatch`
- `missing_segment` - Required segment is missing
- `extra_segment`

### Example Error Info

```python
{
    "error_target": "field",
    "error_segment": "ISA",
    "error_field": "ISA15",
    "error_type": "invalid_value",
    "error_explanation": "Invalid usage indicator: 'TEST' instead of 'T'"
}
```

## File Structure Schema

The EDI 834 Trainer uses a modular file structure:

```
src/core/
├── transaction_generator.py           # Main transaction generator
├── envelope_segment_generator.py      # ISA, IEA, GS, GE, ST, SE, BGN + field generators
├── member_segment_generator.py        # NM1, PER, N3, N4, DMG + field generators
└── coverage_segment_generator.py      # N1, INS, REF, DTP, HD, COB + field generators

src/data/
├── ISA_IEA.yaml                      # ISA/IEA segment and field definitions
└── character_sets.yaml               # Character set definitions
```

## Field Definitions Schema

Field definitions are stored in `src/data/envelope_segment_specifications.yaml` with the following structure:

```yaml
segments:
  ISA:
    name: "Interchange Control Header"
    description: "Defines the start of an EDI interchange"
    purpose: "Leading segment that initiates the EDI transaction"
    rules: "Segment contains exactly 16 fields separated by asterisks (*). Ends with tilde (~)."
    required: true
    position: "first"

fields:
  ISA01:
    name: "Authorization Information Qualifier"
    purpose: "Identifies the type of authorization information"
    rules: "Exactly 2 digits. Numbers only. Cannot be blank."
    characterset: "numeric"
    min_length: 2
    max_length: 2
    valid_values: ["00", "01", "02"]
    error_scenarios: ["non_standard_value"]
    required: true
    position: 1
    default: "00"
```

### Field Definition Fields

- `name`: Human-readable field name
- `purpose`: What the field is used for
- `rules`: Validation rules and constraints
- `characterset`: Character set ("numeric", "alpha", "alphanumeric", "printable", "extended")
- `min_length`/`max_length`: Length constraints
- `valid_values`: Array of valid values for this field
- `common_errors`: Common invalid values for error injection
- `error_scenarios`: Types of errors that can occur
- `required`: Whether the field is mandatory
- `position`: Field position in the segment (1-indexed)
- `default`: Default value when generating clean data


## Character Sets Schema

Character sets are defined in `src/data/character_sets.yaml`:

```yaml
numeric: "0123456789"
alpha: "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphanumeric: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
printable: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ *~:>+^"
extended: "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ *~:>+^%[]_{}\\|<>`#$"
```

## Version History

- **v1.0**: Transaction generator with stub segment generations and structure for error injection
- **v2.0**: Modular file structure with envelope/member/coverage separation
- **v2.1**: Error injection system with field and structural error types
- **v2.2**: Shared data system for consistency across segments
- **v2.3**: YAML-driven field definitions with character sets
