# EDI 834 Trainer - Data Schemas

This document defines the data structures and schemas used throughout the EDI 834 Trainer system.

## ISA/IEA Pair Return Schema

The `generate_isa_iea_pair()` function returns a dictionary with the following structure:

```python
{
    "isa_segment": str,      # Complete ISA segment string
    "iea_segment": str,      # Complete IEA segment string
    "error_info": dict|None, # Error details for GRR explanations
    "shared_data": {         # Shared field values for consistency across segments
        "control_number": str,     # Used in ISA13 and IEA02
        "group_count": str,        # Used in IEA01
        "version": str,            # Used in ISA12, GS08, ST03 (future)
        "date": str,               # Used in ISA09, GS04 (future)
        "time": str,               # Used in ISA10, GS05 (future)
        "sender_id": str,          # Used in ISA06, GS02 (future)
        "receiver_id": str,        # Used in ISA08, GS03 (future)
        "sender_qualifier": str,   # Used in ISA05, GS01 (future)
        "receiver_qualifier": str  # Used in ISA07, GS01 (future)
    }
}
```

### Example Return Value

```python
{
    "isa_segment": "ISA*00*          *00*          *ZZ*SENDER_ID      *ZZ*RECEIVER_ID    *250917*1430*^00501*000000001*0*P*:~",
    "iea_segment": "IEA*1*000000001~",
    "error_info": None,  # No errors
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
```

## Error Info Schema

When `with_errors=True`, the `error_info` dictionary contains:

```python
{
    "error_type": str,      # Type of error: "field_error" or "structural_error"
    "error_target": str     # Which field/segment has the error
}
```

### Error Types

**Field Errors:**
- `isa_sender_qualifier` - Wrong or invalid sender qualifier
- `isa_sender_id` - Missing, wrong length, or invalid sender ID
- `isa_receiver_qualifier` - Wrong or invalid receiver qualifier
- `isa_receiver_id` - Missing, wrong length, or invalid receiver ID
- `isa_date` - Wrong format or invalid date
- `isa_time` - Wrong format or invalid time
- `isa_version` - Old or invalid version number
- `isa_acknowledgment_code` - Invalid acknowledgment code
- `isa_usage_indicator` - Invalid usage indicator
- `isa_control` - Missing, wrong length, or invalid control number
- `iea_group_count` - Missing, wrong length, or invalid group count
- `control_number_mismatch` - IEA control number doesn't match ISA control number
- `mismatched_control` - ISA and IEA control numbers don't match
- `incorrect_group_count` - IEA01 count doesn't match actual number of functional groups

**Structural Errors:**
- `missing_entire_envelope` - No ISA and no IEA segments (most common - 40% weight)
- `isa_missing_delimiter` - Missing field delimiter in ISA segment
- `isa_extra_delimiter` - Extra field delimiter in ISA segment
- `isa_missing_terminator` - Missing segment terminator (~) in ISA
- `isa_missing_field` - ISA segment missing a field
- `isa_blank_field` - ISA segment has a blank field
- `iea_missing_delimiter` - Missing field delimiter in IEA segment
- `iea_extra_delimiter` - Extra field delimiter in IEA segment
- `iea_missing_terminator` - Missing segment terminator (~) in IEA
- `iea_missing_field` - IEA segment missing a field
- `iea_blank_field` - IEA segment has a blank field

### Example Error Info

```python
{
    "error_type": "field_error",
    "error_target": "sender_qualifier"
}
```

## Field Definitions Schema

Field definitions are stored in `src/data/field_definitions.yaml` with the following structure:

```yaml
fields:
  ISA05:
    name: "Interchange Sender ID Qualifier"
    purpose: "Identifies the type of sender ID"
    format_type: "alphanumeric"
    format_length: 2
    valid_values: ["ZZ", "12", "30", "31", "32"]
    required: true
    position: 5
    default: "ZZ"
```

### Field Definition Fields

- `name`: Human-readable field name
- `purpose`: What the field is used for
- `format_type`: Data type ("numeric", "alphanumeric", "ascii", "utf-8")
- `format_length`: Exact length or range (e.g., 2, 15, [1, 5])
- `format_encoding`: Character encoding (only if not ASCII)
- `valid_values`: Array of valid values for this field
- `required`: Whether the field is mandatory
- `position`: Field position in the segment (1-indexed)
- `default`: Default value when generating clean data

## Future Schema Extensions

### GS/GE Segment Schema (v7.0+)

When GS/GE segments are added, the return schema will be extended:

```python
{
    "isa_segment": str,
    "gs_segment": str,      # New: GS segment
    "st_segment": str,      # New: ST segment  
    "transaction_data": {}, # New: 834 transaction segments
    "se_segment": str,      # New: SE segment
    "ge_segment": str,      # New: GE segment
    "iea_segment": str,
    "error_info": dict|None,
    "shared_data": {
        # Existing fields plus:
        "functional_group_id": str,    # Used in GS01, GE01
        "application_sender": str,     # Used in GS02
        "application_receiver": str,   # Used in GS03
        "transaction_set_id": str,     # Used in ST01, SE01
        "transaction_count": str,      # Used in SE02
        # ... etc
    }
}
```

### 999 Acknowledgment Schema (v8.0+)

When 999 acknowledgments are added:

```python
{
    "isa_segment": str,
    "gs_segment": str,
    "st_segment": str,
    "ak1_segment": str,     # New: AK1 segment
    "ak2_segment": str,     # New: AK2 segment
    "ak5_segment": str,     # New: AK5 segment
    "ak9_segment": str,     # New: AK9 segment
    "se_segment": str,
    "ge_segment": str,
    "iea_segment": str,
    "error_info": dict|None,
    "shared_data": {
        # Existing fields plus acknowledgment-specific fields
    }
}
```

## Version History

- **v1.0**: Basic ISA/IEA pair with tuple return
- **v1.1**: Dictionary return with shared_data for consistency
- **v7.0**: Extended schema for full 834 transactions
- **v8.0**: Extended schema for 999 acknowledgments
