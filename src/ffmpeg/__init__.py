from .executable import add_to_path, get_executable_path

__version__ = "0.0.1"

FFMPEG_PATH = get_executable_path()


def run() -> None:
    import subprocess
    import sys

    subprocess.run([FFMPEG_PATH, *sys.argv[1:]])


def run_as_ffmpeg(command: str) -> None:
    import subprocess

    subprocess.run([FFMPEG_PATH, command])
