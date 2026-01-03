import os


def __get_hook_dirs() -> list[str]:
    return [os.path.dirname(__file__)]


def __get_tests() -> list[str]:
    return [os.path.dirname(__file__)]
