import warnings

from .executable import add_to_path, get_executable_path

__version__ = "0.0.2"

FFMPEG_PATH = get_executable_path()
if FFMPEG_PATH is None:
    warnings.warn(
        "ffmpeg binaries not found. Please call ffmpeg.init() to download them."
    )


def run_as_ffmpeg(command: str) -> None:
    import subprocess

    subprocess.run([FFMPEG_PATH, command])


def init() -> None:
    global FFMPEG_PATH
    FFMPEG_PATH = get_executable_path(ensure_binaries=True)
