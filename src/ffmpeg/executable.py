import pathlib

from .internals import get_binaries


def get_executable_path() -> pathlib.Path:
    return get_binaries()


def add_to_path() -> None:
    pass
