import pathlib
import pytest
import sys
import ffmpeg.executable as executable

from unittest.mock import patch


def test_get_executable_path_success():
    with patch("ffmpeg.executable.get_binaries") as mock_get_path:
        b = pathlib.Path("binary")
        p = pathlib.Path("probe")
        mock_get_path.return_value = (b, p)

        paths = executable.get_executable_path(ensure_binaries=False)

        assert paths == (b, p)


def test_get_executable_path_failed_no_ensure():
    with (
        patch("ffmpeg.executable.get_binaries") as mock_get_path,
        patch("ffmpeg.executable.download_binaries") as mock_download,
    ):
        mock_get_path.return_value = None

        paths = executable.get_executable_path(ensure_binaries=False)

        assert paths == (None, None)
        mock_download.assert_not_called()


def test_get_executable_success_with_download():
    with (
        patch("ffmpeg.executable.get_binaries") as mock_get_path,
        patch("ffmpeg.executable.download_binaries") as mock_download,
    ):
        b = pathlib.Path("binary")
        p = pathlib.Path("probe")
        mock_get_path.side_effect = [None, (b, p)]

        paths = executable.get_executable_path(ensure_binaries=True)

        assert paths == (b, p)
        mock_download.assert_called_once()


def test_get_executable_failed_with_download():
    with (
        patch("ffmpeg.executable.get_binaries") as mock_get_path,
        patch("ffmpeg.executable.download_binaries") as mock_download,
    ):
        mock_get_path.return_value = None

        with pytest.raises(RuntimeError):
            executable.get_executable_path(ensure_binaries=True)
        mock_download.assert_called_once()


def test_run():
    with (
        patch("ffmpeg.executable.get_binaries") as mock_get_path,
        patch("subprocess.run") as mock_run,
        patch.object(sys, "argv", ["script", "arg1", "arg2"]),
    ):
        b = pathlib.Path("binary")
        p = pathlib.Path("probe")
        mock_get_path.return_value = (b, p)

        executable._run()

        mock_run.assert_called_once()
        mock_run.assert_called_with([str(b), "arg1", "arg2"])


def test_run_no_binaries():
    with (
        patch("ffmpeg.executable.get_binaries") as mock_get_path,
        patch("subprocess.run") as mock_run,
        patch.object(sys, "argv", ["script", "arg1", "arg2"]),
        patch("ffmpeg.executable.download_binaries") as mock_download,
    ):
        mock_get_path.return_value = None

        with pytest.raises(RuntimeError):
            executable._run()

        mock_run.assert_not_called()
        mock_download.assert_called_once()
        assert mock_get_path.call_count == 2
