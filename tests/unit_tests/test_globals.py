import ffmpeg
import pathlib


def test_executable_constant():
    assert isinstance(ffmpeg.FFMPEG_PATH, pathlib.Path)
