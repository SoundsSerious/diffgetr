# diffgetr

A Python library for comparing nested data structures with detailed diff reporting.

## Features

- Compare deeply nested dictionaries and lists.
- Summarize differences with key frequency counts.
- Command-line tool to diff two JSON files and navigate to specific paths.

## Installation

```bash
pip install .
```

## Usage

### As a Library

```python
from diff_get import diff_get

diff = diff_get(obj1, obj2)
print(diff)  # Prints a summary of differences
```

### Command Line

```bash
diffgetr file1.json file2.json path.to.key
```

- `file1.json`, `file2.json`: JSON files to compare.
- `path.to.key`: Dot-separated path to navigate (e.g., `foo.bar[0].baz`).

## License

MIT
