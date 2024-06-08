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

Here's a simple example that converts a video file to an audio file:

```python
from streampot import StreamPot

client = StreamPot(secret='yourToken')

job = client.input('https://download.samplelib.com/mp4/sample-5s.mp4') \
    .output('audio.mp3') \
    .run_and_wait()

print(job.outputs['audio.mp3'])
```

If you want to run the job in the background, you can use the `run` method:

```python
job = client.input('https://download.samplelib.com/mp4/sample-5s.mp4') \
    .output('audio.mp3') \
    .run()
```

And fetch the job info using the `get_job` method:

```python
job = client.get_job(job.id)

print(job.status)
print(job.outputs['audio.mp3'])  # output url by file name
print(job.logs)  # error logs if any
print(job.created_at)
print(job.completed_at)
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
