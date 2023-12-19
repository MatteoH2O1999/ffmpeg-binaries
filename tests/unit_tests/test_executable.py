import os
import pathlib
import pytest
import sys
import ffmpeg.executable as executable

from unittest.mock import patch


def test_run():
    with patch("ffmpeg.executable.get_binaries") as mock_get_path, patch(
        "subprocess.run"
    ) as mock_run, patch.object(sys, "argv", ["script", "arg1", "arg2"]):
        b = pathlib.Path("binary")
        p = pathlib.Path("probe")
        mock_get_path.return_value = (b, p)

        executable._run()

        mock_run.assert_called_once()
        mock_run.assert_called_with([str(b), "arg1", "arg2"])


def test_run_no_binaries():
    with patch("ffmpeg.executable.get_binaries") as mock_get_path, patch(
        "subprocess.run"
    ) as mock_run, patch.object(sys, "argv", ["script", "arg1", "arg2"]), patch(
        "ffmpeg.executable.download_binaries"
    ) as mock_download:
        mock_get_path.return_value = None

        with pytest.raises(RuntimeError):
            executable._run()

        mock_run.assert_not_called()
        mock_download.assert_called_once()
        assert mock_get_path.call_count == 2


def test_add_to_path():
    with patch("ffmpeg.executable.get_binaries") as mock_get_path, patch.object(
        os, "environ", {"PATH": "path1"}
    ) as mock_environ:
        b = pathlib.Path("binary")
        p = pathlib.Path("probe")
        mock_get_path.return_value = (b, p)

        executable.add_to_path()

        assert mock_environ["PATH"].split(os.pathsep).sort() == ["path1", str(b)].sort()


def test_add_to_path_no_binaries():
    with patch("ffmpeg.executable.get_binaries") as mock_get_path, patch.object(
        os, "environ", {"PATH": "path1"}
    ) as mock_environ, patch("ffmpeg.executable.download_binaries") as mock_download:
        mock_get_path.return_value = None

        with pytest.raises(RuntimeError):
            executable.add_to_path()

        assert mock_environ["PATH"] == "path1"
        mock_download.assert_called_once()
        assert mock_get_path.call_count == 2
