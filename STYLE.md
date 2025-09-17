# EDI Trainer Style Guide

This document outlines the coding style and preferences for the EDI Trainer project.

## Python Style

### Type Hints
- **Use type hints as documentation only** - no enforcement
- Use built-in types: `str`, `bool`, `int`, `tuple`, `list`, `dict`
- **Do NOT import from `typing`** - avoid `List[str]`, `Optional[str]`, etc.
- Type hints should be simple and readable

```python
# Good
def generate_segment(with_errors: bool = False) -> str:
    return "ISA*..."

# Bad
from typing import Optional, List
def generate_segment(with_errors: bool = False) -> Optional[str]:
    return "ISA*..."
```

### Code Style
- **PEP 8 compliant** - use `black` formatter
- **Simple, minimal code** - avoid overengineering
- **Single responsibility** - one function, one purpose
- **No unnecessary classes** - prefer functions over classes
- **Clear, descriptive names** - avoid abbreviations

### Comments
- **Explain WHY, not WHAT** - focus on reasoning, not restating code
- **Docstrings for all functions** - explain purpose and parameters
- **Inline comments for complex logic** - explain business rules

```python
# Good - explains why
# Use realistic error prevalence based on production data
error_type = random.choices(["missing", "wrong_length"], weights=[40, 30])

# Bad - restates what code does
# Choose error type randomly
error_type = random.choice(["missing", "wrong_length"])
```

## Project Structure

### File Organization
- **One concept per file** - segment generators, error generators, etc.
- **Clear module names** - `segment_generators.py`, not `segments.py`
- **Archive old versions** - keep `archive/` folder for reference

### Dependencies
- **Minimal dependencies** - only essential libraries
- **No separate type libraries** - avoid `mypy`, `typing-extensions`
- **Essential libraries only**: `faker`, `fastapi` (for API), `pytest` (for tests)

## EDI-Specific Guidelines

### Error Generation
- **Realistic error prevalence** - based on actual production data
- **Single error per segment** - more educational than multiple errors
- **Systematic approach** - each field type has its own generator
- **GRR methodology** - scaffolded learning with explanations

### Segment Structure
- **ISA/IEA as pairs** - they must have matching control numbers
- **Generate valid first** - then introduce one error
- **Structural vs field errors** - handle both levels appropriately

## Teaching Philosophy

### Learning Approach
- **Constructivist teaching** - scaffolded learning with hints
- **Progressive difficulty** - clean data → errors → explanations
- **Real-world scenarios** - errors that actually occur in production
- **Actionable feedback** - specific, helpful error messages

### Documentation
- **Clear examples** - show both clean and error cases
- **Progressive complexity** - start simple, add complexity
- **Real-world context** - explain why errors matter

## Open Source Considerations

### License
- **Creative Commons Attribution-NonCommercial 4.0** - free for non-commercial use
- **Attribution required** - credit original author
- **No commercial use** - prevents exploitation

### Contributing
- **Clear contribution guidelines** - document how to contribute
- **Issue templates** - structured bug reports and feature requests
- **Pull request templates** - ensure quality contributions
- **Code of conduct** - welcoming environment for all contributors

### Documentation
- **README.md** - clear project overview and quick start
- **API documentation** - for REST API endpoints
- **Learning guides** - how to use GRR methodology
- **Error reference** - complete list of error types

### Testing
- **Unit tests** - test individual functions
- **Integration tests** - test complete workflows
- **Example-based tests** - test with real EDI data
- **Error scenario tests** - ensure error generation works

### CI/CD
- **Automated testing** - run tests on every commit
- **Code formatting** - enforce style with `black`
- **Linting** - catch common issues with `flake8`
- **Documentation building** - ensure docs stay current

### Release Management
- **Semantic versioning** - clear version numbering
- **Changelog** - document what changed
- **Release notes** - highlight new features
- **Backward compatibility** - don't break existing functionality

## Tools and Workflow

### Development Tools
- **Black** - code formatting
- **Flake8** - linting
- **Pytest** - testing
- **Faker** - test data generation

### Git Workflow
- **Feature branches** - one feature per branch
- **Clear commit messages** - explain what and why
- **Pull request reviews** - ensure code quality
- **Squash commits** - clean history

### File Naming
- **Snake case** - `segment_generators.py`
- **Descriptive names** - `error_generators.py`, not `errors.py`
- **Consistent patterns** - `generate_*` for generators, `get_*` for getters

## Performance Considerations

### Code Performance
- **Simple algorithms** - avoid premature optimization
- **Efficient data structures** - use appropriate types
- **Minimal memory usage** - don't load unnecessary data
- **Fast startup** - quick to import and use

### User Experience
- **Fast generation** - quick EDI file creation
- **Clear feedback** - immediate error explanations
- **Progressive loading** - show progress for large batches
- **Responsive interface** - quick response times

This style guide ensures the EDI Trainer remains simple, educational, and maintainable while following Python best practices and open source conventions.
