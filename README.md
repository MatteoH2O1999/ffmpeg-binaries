# ffmpeg for Python

[![CI/CD](https://github.com/MatteoH2O1999/ffmpeg-binaries/actions/workflows/ci.yml/badge.svg)](https://github.com/MatteoH2O1999/ffmpeg-binaries/actions/workflows/ci.yml)
[![codecov](https://codecov.io/github/MatteoH2O1999/ffmpeg-binaries/graph/badge.svg?token=9jkgMvjxxs)](https://codecov.io/github/MatteoH2O1999/ffmpeg-binaries)
![GitHub](https://img.shields.io/github/license/MatteoH2O1999/ffmpeg-binaries)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - Version](https://img.shields.io/pypi/v/ffmpeg-binaries?label=pypi%20package&color=green)](https://pypi.org/project/ffmpeg-binaries/)
[![PyPI - Version Mirror](https://img.shields.io/pypi/v/ffmpeg-binaries-compat?label=pypi%20mirror%20package&color=green)](https://pypi.org/project/ffmpeg-binaries-compat/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ffmpeg-binaries)
[![Downloads](https://img.shields.io/pepy/dt/ffmpeg-binaries?label=downloads&color=blue)](https://pepy.tech/project/ffmpeg-binaries)
[![Mirror Downloads](https://img.shields.io/pepy/dt/ffmpeg-binaries-compat?label=mirror%20downloads&color=blue)](https://pepy.tech/project/ffmpeg-binaries-compat)

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

# Call ffprobe directly
ffmpeg.run_as_ffprobe("-h")

# Use the binaries path in other modules
other_module.add_ffmpeg(ffmpeg.FFMPEG_PATH)

# Add directly to path
ffmpeg.add_to_path()
```

## Import name conflict

If another dependency aleady uses the `ffmpeg` import name, like [typed-ffmpeg](https://github.com/livingbio/typed-ffmpeg) or
[ffmpeg-python](https://github.com/kkroening/ffmpeg-python), you can install the mirror package instead:

```commandline
pip install ffmpeg-binaries-compat
```

and use it with the import name `ffmpeg_binaries`:

```python
import ffmpeg_binaries as ffmpeg

# Initialize module (only if no binaries found)
ffmpeg.init()

# Call ffmpeg directly
ffmpeg.run_as_ffmpeg("-h")

# Call ffprobe directly
ffmpeg.run_as_ffprobe("-h")

# Use the binaries path in other modules
other_module.add_ffmpeg(ffmpeg.FFMPEG_PATH)

# Add directly to path
ffmpeg.add_to_path()
```
