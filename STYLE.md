# EDI Trainer - Architectural Style Guide

## Error Generation Pattern

### Field Error Generators
- **Signature**: `generator(field_designation, field_spec, valid_value, error_info=None)`
- **Behavior**: Update `error_info` dictionary directly, return just the error value string
- **DO NOT**: Return dictionaries 

### Structural Error Generators  
- **Signature**: `structural_error_generator(error_type, field_values=None, error_info=None)`
- **Behavior**: Update `error_info` dictionary directly, return just the modified segment string
- **Fallback**: Return empty string for missing segments

### Error Info Dictionary
- **Pattern**: Mutable dictionary passed by reference through entire call chain
- **Updates**: Error generators directly modify the shared dictionary
- **Return**: Generators return only the error value, not full dictionaries

## Field Generation Architecture

### Segment Generators
- **Location**: Field generators live in segment generator files (e.g., `envelope_segment_generator.py`)
- **Pattern**: Each field has its own generator function with clear English names
- **Grouping**: Field generators grouped by segment with clear section headers
- **Data Sources**: Field generators call appropriate helper functions from `data_generator.py`

### Data Generator Role
- **Purpose**: Helper functions used across segment generators
- **DO NOT**: Import field generators from `data_generator.py`
- **Functions**: `random_string_generator`, `random_faker_generator`, `pick_valid_value`, etc.

### Field Generator Pattern
```python
def generate_field_name(error_target=None, error_info=None):
    # 1. Generate valid value using data generator helpers
    valid_value = random_faker_generator("company", 15, 15)
    
    # 2. Check if this field should have an error
    if error_target == "ISA06":
        return apply_field_error("ISA06", field_spec, valid_value, error_info)
    
    # 3. Return valid value
    return valid_value
```

## Segment Generation Flow

### Error Injection Logic
1. **Generate all valid field values** into a list
2. **Apply error to targeted field** by index if needed
3. **Join list** to form segment string
4. **Handle structural errors** after building valid segment

### Field Values List Pattern
```python
field_values = [
    generate_auth_qualifier(error_target, error_info),
    generate_security_qualifier(error_target, error_info),
    # ... etc
]
segment = f"ISA*{'*'.join(field_values)}~"
```

## Error Message Formatting

### Smart Join for Valid Values
- **Function**: `smart_join(items, final_joiner=" or ")`
- **Result**: `'A'`, `'A or B'`, `'A, B or C'`
- **Rationale**: No Oxford comma in logical expressions (looks like shopping list)

### Error Explanations
- **Format**: `"{field_designation} contains {error_type} '{error_value}' not {valid_list}"`
- **Example**: `"ISA15 contains invalid value 'NA' not 'P' or 'T'"`
- **DO NOT**: Use redundant prefixes like "Field " or "Required field "

## Code Organization

### File Responsibilities
- **`data_generator.py`**: Core helper functions, no field-specific logic
- **`envelope_segment_generator.py`**: ISA/IEA field generators + segment building
- **`error_generator.py`**: Individual error type generators
- **`transaction_generator.py`**: Orchestrates segment generation

### TODO Management
- **Location**: In-file comments with specific implementation notes
- **Format**: Clear, actionable items with context
- **Updates**: Mark completed items, add new ones as needed

## Common Mistakes to Avoid

### Architectural Violations
- ❌ Returning dictionaries from error generators
- ❌ Creating field generators in `data_generator.py`

### Pattern Violations
- ❌ If/elif/else chains in segment generators
- ❌ Individual field error checking in segment generators  
- ❌ Importing field generators from `data_generator.py`
- ❌ Using `generate_valid_value` or `generate_field_value` abstractions


## Testing Philosophy
- **User Preference**: Ask before running tests, don't auto-execute
- **Reminder**: It's okay to remind user to run tests
- **Manual Control**: User likes to run command line themselves for practice
