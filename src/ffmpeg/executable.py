import pathlib
import warnings

from .internals import download_binaries, get_binaries
from typing import Tuple, Union


def get_executable_path(
    ensure_binaries: bool = False,
) -> Tuple[Union[pathlib.Path, None], Union[pathlib.Path, None]]:
    binaries_path = get_binaries()
    if binaries_path is None and ensure_binaries:
        warnings.warn("ffmpeg binaries not found. Will download binaries now.")
        download_binaries()
        binaries_path = get_binaries()
        if binaries_path is None:
            raise RuntimeError("Could not download correct ffmpeg binaries.")
    if binaries_path is None:
        return None, None
    return binaries_path


def _run() -> None:
    import subprocess
    import sys

    subprocess.run([str(get_executable_path(ensure_binaries=True)[0]), *sys.argv[1:]])
