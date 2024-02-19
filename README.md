# ffmpeg for Python

[![CI/CD](https://github.com/MatteoH2O1999/ffmpeg-binaries/actions/workflows/ci.yml/badge.svg)](https://github.com/MatteoH2O1999/ffmpeg-binaries/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/MatteoH2O1999/ffmpeg-binaries/graph/badge.svg?token=9jkgMvjxxs)](https://codecov.io/github/MatteoH2O1999/ffmpeg-binaries)
![GitHub](https://img.shields.io/github/license/MatteoH2O1999/ffmpeg-binaries)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI Version](https://badge.fury.io/py/ffmpeg-binaries.svg)](https://pypi.org/project/ffmpeg-binaries/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ffmpeg-binaries)
[![Downloads](https://pepy.tech/badge/ffmpeg-binaries)](https://pepy.tech/project/ffmpeg-binaries)

Static builds of ffmpeg for Python

## Installation

From pip:

```commandline
pip install ffmpeg-binaries
```

## Basic usage

```python
import ffmpeg

# Initialize module (only if no binaries found)
ffmpeg.init()

# Call ffmpeg directly
ffmpeg.run_as_ffmpeg("-h")

# Use the binaries path in other modules
other_module.add_ffmpeg(ffmpeg.FFMPEG_PATH)

# Add directly to path
ffmpeg.add_to_path()
```
