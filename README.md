[![PyPI](https://img.shields.io/pypi/v/streampot.svg)](https://pypi.org/project/streampot/)
[![Tests](https://github.com/StreamPot/python-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/StreamPot/python-sdk/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/StreamPot/python-sdk?include_prereleases&label=changelog)](https://github.com/StreamPot/python-sdk/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/StreamPot/python-sdk/blob/main/LICENSE)

## Installation

Install this library using `pip`:
```bash
pip install streampot
```
## Usage

```python
from streampot import StreamPot

client = StreamPot(secret='yourToken')
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:
```bash
cd streampot
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
