# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**diffgetr** is a Python library for comparing nested data structures with detailed diff reporting and interactive navigation. It provides advanced diff capabilities beyond basic comparison, featuring pattern recognition, multiple output formats, and dictionary-like navigation through diff results.

## Installation and Development Commands

```bash
# Install the package locally
pip install .

# Install in development mode 
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Test the command line tool
diffgetr file1.json file2.json path.to.key
```

## Testing Commands

```bash
# Run unit tests
python -m unittest discover tests -v

# Build and test package
python -m build
pip install dist/*.whl
python -c "import diffgetr; print('Package imported successfully')"
```

## Core Architecture

### Main Class: `diff_get`

The library centers around a single class `diff_get` located in `diffgetr/diff_get.py:9`. This class:

1. **Wraps DeepDiff**: Uses the `deepdiff` library as the underlying comparison engine with configurable parameters (`diffgetr/diff_get.py:22-24`)

2. **Enables Navigation**: Implements `__getitem__` to allow dictionary-like traversal through nested diff results (`diffgetr/diff_get.py:35-41`)

3. **Type Coercion**: Automatically converts lists/tuples to dictionaries for consistent comparison (`diffgetr/diff_get.py:14-17`)

4. **Location Tracking**: Maintains path context through the `loc` property for debugging and display (`diffgetr/diff_get.py:26-33`)

### Key Features

#### Interactive Navigation (`diffgetr/diff_get.py:35-57`)
- Dictionary-style access: `diff['key1']['nested_key']`
- IPython tab completion support via `_ipython_key_completions_`
- Error handling with context-aware KeyError messages

#### Multiple Output Formats
- **Summary**: Pattern recognition with frequency counts (`diff_summary()` at `diffgetr/diff_get.py:239-292`)
- **Detailed**: Full diff with pretty printing (`diff_all()` at `diffgetr/diff_get.py:96-109`)
- **Side-by-side**: Tabular comparison with percentage changes (`diff_sidebyside()` at `diffgetr/diff_get.py:111-237`)

#### Pattern Recognition (`diffgetr/diff_get.py:260-264`)
- UUID detection and abstraction
- CSV-like number sequence recognition
- Path normalization for cleaner summaries

### Command Line Interface

Entry point defined in `pyproject.toml:29` as `diffgetr = "diffgetr.diff_get:main"`

The CLI (`main()` function at `diffgetr/diff_get.py:295-329`) supports:
- JSON file comparison
- Dot-notation path navigation
- Array index navigation with bracket notation

### Configuration Options

#### DeepDiff Parameters (`diffgetr/diff_get.py:21-24`)
Default settings:
- `ignore_numeric_type_changes=True`
- `significant_digits=3`

Can be overridden via `deep_diff_kw` parameter.

#### Behavior Modifiers
- `ignore_added=False`: Filter out added items to focus on changes/removals
- Configurable precision for numeric comparisons
- Threshold-based filtering in side-by-side output

## Development Notes

### Code Structure
- Single module design with one main class
- Heavy use of property decorators for computed values
- String/bytes handling for flexible output streams
- Recursive instantiation for navigation

### Key Dependencies
- `deepdiff>=6.0.0`: Core comparison engine
- Standard library: `json`, `re`, `argparse`, `pprint`

### Testing Approach
The library includes comprehensive examples in the README showing various use cases. When adding features, ensure compatibility with existing navigation patterns and output formats.