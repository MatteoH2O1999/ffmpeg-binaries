import ffmpeg
import importlib
import pathlib
import warnings

from unittest.mock import patch


def test_executable_constant_if_binaries_installed():
    with patch("ffmpeg.executable.get_binaries") as mock_get_binaries:
        b = pathlib.Path("binary")
        p = pathlib.Path("probe")
        mock_get_binaries.return_value = (b, p)

        importlib.reload(ffmpeg)

        assert ffmpeg.FFMPEG_PATH is b
        assert ffmpeg.FFPROBE_PATH is p
        assert ffmpeg.FFMPEG_FOLDER == p.parent


def test_executable_constant_if_binaries_not_installed():
    with patch(
        "ffmpeg.executable.get_binaries"
    ) as mock_get_binaries, warnings.catch_warnings(record=True) as w:
        mock_get_binaries.return_value = None

        importlib.reload(ffmpeg)

        assert ffmpeg.FFMPEG_PATH is None
        assert ffmpeg.FFPROBE_PATH is None
        assert ffmpeg.FFMPEG_FOLDER is None
        assert len(w) == 1
        warning = w[0].message
        assert isinstance(warning, Warning)
        assert "ffmpeg.init()" in str(warning)


def test_init():
    with patch("ffmpeg.get_executable_path") as mock_get_executable:
        b = pathlib.Path("binary")
        p = pathlib.Path("probe")
        mock_get_executable.return_value = (b, p)

        ffmpeg.init()

        assert ffmpeg.FFMPEG_PATH is b
        assert ffmpeg.FFPROBE_PATH is p
        assert ffmpeg.FFMPEG_FOLDER == p.parent
        mock_get_executable.assert_called_once()
        mock_get_executable.assert_called_with(ensure_binaries=True)


def test_as_ffmpeg():
    with patch("subprocess.run") as mock_run:
        p = pathlib.Path("binaries")
        ffmpeg.FFMPEG_PATH = p

        ffmpeg.run_as_ffmpeg("command")

        mock_run.assert_called_once()
        mock_run.assert_called_with([p, "command"])
