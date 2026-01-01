import warnings

from .executable import get_executable_path

__version__ = "1.1.0"

FFMPEG_PATH, FFPROBE_PATH = get_executable_path()
if FFMPEG_PATH is None:
    FFMPEG_FOLDER = None
    warnings.warn(
        "ffmpeg binaries not found. Please call ffmpeg.init() to download them."
    )
else:
    FFMPEG_FOLDER = FFMPEG_PATH.parent


def run_as_ffmpeg(command: str) -> int:
    """
    Run the command as ffmpeg
    :param command: The command to run
    :return: The command exit code
    """
    import subprocess

    return subprocess.run([FFMPEG_PATH, command]).returncode


def run_as_ffprobe(command: str) -> int:
    """
    Run the command as ffprobe
    :param command: The command to run
    :return: The command exit code
    """
    import subprocess

    return subprocess.run([FFPROBE_PATH, command]).returncode


def init() -> None:
    """
    Init ffmpeg global variables
    """
    global FFMPEG_PATH, FFPROBE_PATH, FFMPEG_FOLDER
    FFMPEG_PATH, FFPROBE_PATH = get_executable_path(ensure_binaries=True)
    FFMPEG_FOLDER = FFMPEG_PATH.parent


def add_to_path() -> None:
    """
    Add ffmpeg binaries to path by prepending FFMPEG_FOLDER to PATH
    """
    import os

    if FFMPEG_FOLDER is None:
        init()
    os.environ["PATH"] = f"{str(FFMPEG_FOLDER)}{os.pathsep}{os.environ['PATH']}"


def is_on_path() -> bool:
    """
    Check whether FFMPEG_FOLDER is already on PATH (not whether it is the first, so other ffmpeg installations may have priority)
    """
    import os

    if FFMPEG_FOLDER is None:
        return False
    return str(FFMPEG_FOLDER) in os.environ["PATH"].split(os.pathsep)


def use_ffmpeg(ffmpeg_path: str, ffprobe_path: str) -> None:
    """
    Use a custom ffmpeg path instead of the builtin one.
    :param ffmpeg_path: The path to ffmpeg executable
    :param ffprobe_path: The path to ffprobe executable
    """
    import pathlib

    if not ffmpeg_path or not ffprobe_path:
        raise ValueError("Both paths must be specified")

    ffmpeg_pathlib = pathlib.Path(ffmpeg_path)
    ffprobe_pathlib = pathlib.Path(ffprobe_path)
    if not ffmpeg_pathlib.exists():
        raise ValueError(f"Expected a valid path for ffmpeg, got {ffmpeg_path}")
    if not ffmpeg_pathlib.is_file():
        raise ValueError(f"Expected a valid file for ffmpeg, got {ffmpeg_path}")
    if not ffprobe_pathlib.exists():
        raise ValueError(f"Expected a valid path for ffprobe, got {ffprobe_path}")
    if not ffprobe_pathlib.is_file():
        raise ValueError(f"Expected a valid file for ffprobe, got {ffprobe_path}")
    ffmpeg_folder_path = ffmpeg_pathlib.parent
    if not ffmpeg_folder_path == ffprobe_pathlib.parent:
        raise ValueError(
            f"Expected ffmpeg and ffprobe to be in the same folder, got {str(ffmpeg_pathlib.parent)} and {str(ffprobe_pathlib.parent)}"
        )

    global FFMPEG_PATH, FFPROBE_PATH, FFMPEG_FOLDER
    FFMPEG_PATH = ffmpeg_pathlib
    FFPROBE_PATH = ffprobe_pathlib
    FFMPEG_FOLDER = ffmpeg_folder_path
