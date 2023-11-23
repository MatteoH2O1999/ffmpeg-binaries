import os
import pathlib
import warnings

from .internals import download_binaries, get_binaries
from typing import Union


def get_executable_path(ensure_binaries: bool = False) -> Union[pathlib.Path, None]:
    binaries_path = get_binaries()
    if binaries_path is None and ensure_binaries:
        warnings.warn("ffmpeg binaries not found. Will download binaries now.")
        download_binaries()
        binaries_path = get_binaries()
        if binaries_path is None:
            raise RuntimeError("Could not download correct ffmpeg binaries.")
    return binaries_path


def add_to_path() -> None:
    path_to_add = get_executable_path(ensure_binaries=True)
    os.environ["PATH"] = f"{str(path_to_add)}{os.pathsep}{os.environ['PATH']}"


def _run() -> None:
    import subprocess
    import sys

    subprocess.run([str(get_executable_path(ensure_binaries=True)), *sys.argv[1:]])
