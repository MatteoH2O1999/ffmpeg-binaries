import os
import ffmpeg
import importlib
import pathlib
import pytest
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
    with (
        patch("ffmpeg.executable.get_binaries") as mock_get_binaries,
        warnings.catch_warnings(record=True) as w,
    ):
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


def test_as_ffprobe():
    with patch("subprocess.run") as mock_run:
        p = pathlib.Path("binaries")
        ffmpeg.FFPROBE_PATH = p

        ffmpeg.run_as_ffprobe("command")

        mock_run.assert_called_once()
        mock_run.assert_called_with([p, "command"])


def test_add_to_path():
    with patch.object(os, "environ", {"PATH": "path1"}) as mock_environ:
        b = pathlib.Path("bin/binary")
        p = pathlib.Path("bin/probe")

        ffmpeg.FFMPEG_PATH = b
        ffmpeg.FFMPEG_FOLDER = b.parent
        ffmpeg.FFPROBE_PATH = p

        ffmpeg.add_to_path()

        expected = ["path1", str(b.parent)]
        expected.sort()
        actual = mock_environ["PATH"].split(os.pathsep)
        actual.sort()

        assert actual == expected


def test_add_to_path_no_binaries():
    with (
        patch("ffmpeg.executable.get_binaries") as mock_get_path,
        patch.object(os, "environ", {"PATH": "path1"}) as mock_environ,
    ):
        ffmpeg.FFMPEG_PATH = None
        ffmpeg.FFMPEG_FOLDER = None
        ffmpeg.FFPROBE_PATH = None

        b = pathlib.Path("bin/binary")
        p = pathlib.Path("bin/probe")
        mock_get_path.return_value = (b, p)

        ffmpeg.add_to_path()

        expected = ["path1", str(b.parent)]
        expected.sort()
        actual = mock_environ["PATH"].split(os.pathsep)
        actual.sort()

        assert actual == expected


def test_is_on_path():
    with patch.object(os, "environ", {"PATH": "path1"}) as mock_environ:
        ffmpeg.FFMPEG_PATH = None
        ffmpeg.FFMPEG_FOLDER = None
        ffmpeg.FFPROBE_PATH = None

        assert ffmpeg.is_on_path() is False

        b = pathlib.Path("bin/binary")
        p = pathlib.Path("bin/probe")

        ffmpeg.FFMPEG_PATH = b
        ffmpeg.FFMPEG_FOLDER = b.parent
        ffmpeg.FFPROBE_PATH = p

        assert ffmpeg.is_on_path() is False

        ffmpeg.add_to_path()

        assert ffmpeg.is_on_path() is True


def test_use_ffmpeg_null_ffmpeg_path():
    b = "bin/binary"
    p = None
    with pytest.raises(ValueError):
        ffmpeg.use_ffmpeg(b, p)


def test_use_ffmpeg_null_ffprobe_path():
    b = None
    p = "bin/probe"
    with pytest.raises(ValueError):
        ffmpeg.use_ffmpeg(b, p)


def test_use_ffmpeg_null_paths():
    b = None
    p = None
    with pytest.raises(ValueError):
        ffmpeg.use_ffmpeg(b, p)


def test_use_ffmpeg_fail():
    b = None
    p = None
    ffmpeg.FFMPEG_PATH = pathlib.Path("bin/binary")
    ffmpeg.FFPROBE_PATH = pathlib.Path("bin/probe")
    ffmpeg.FFMPEG_FOLDER = ffmpeg.FFMPEG_PATH.parent

    with pytest.raises(ValueError):
        ffmpeg.use_ffmpeg(b, p)

    assert ffmpeg.FFMPEG_PATH == pathlib.Path("bin/binary")
    assert ffmpeg.FFPROBE_PATH == pathlib.Path("bin/probe")
    assert ffmpeg.FFMPEG_FOLDER == pathlib.Path("bin")


def test_use_ffmpeg_success():
    with (
        patch("pathlib.Path.exists", new=lambda _: True),
        patch("pathlib.Path.is_file", new=lambda _: True),
    ):
        b = "newbin/binary"
        p = "newbin/probe"
        ffmpeg.FFMPEG_PATH = pathlib.Path("bin/binary")
        ffmpeg.FFPROBE_PATH = pathlib.Path("bin/probe")
        ffmpeg.FFMPEG_FOLDER = ffmpeg.FFMPEG_PATH.parent

        ffmpeg.use_ffmpeg(b, p)

        assert ffmpeg.FFMPEG_PATH == pathlib.Path("newbin/binary")
        assert ffmpeg.FFPROBE_PATH == pathlib.Path("newbin/probe")
        assert ffmpeg.FFMPEG_FOLDER == pathlib.Path("newbin")
