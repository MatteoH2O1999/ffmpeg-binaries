import functools
import json
import os
import shutil
import subprocess
import sys
import pathlib
import re

from typing import List, TypedDict, Tuple, Union
from .downloader import _Downloader
from .mac import _MacDownloader
from .nix import _NixDownloader
from .win import _WinDownloader


FFMPEG_RE = re.compile(r"ffmpeg version (?P<version>\d+\.?\d*\.?\d*)")


class _BinariesURL(TypedDict):
    win: List[str]
    nix: List[str]
    mac: List[str]


class _BinariesJSON(TypedDict):
    version: str
    url: _BinariesURL


@functools.total_ordering
class _SemverVersion:
    def __init__(self, string_version: str):
        split_version = string_version.split(".")
        while len(split_version) != 3:
            split_version.append("0")

        self.major = int(split_version[0])
        self.minor = int(split_version[1])
        self.patch = int(split_version[2])

    def __eq__(self, other):
        if not isinstance(other, _SemverVersion):
            return False
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
        )

    def __gt__(self, other):
        if not isinstance(other, _SemverVersion):
            raise NotImplementedError
        if self.major == other.major:
            if self.minor == other.minor:
                if self.patch == other.patch:
                    return False
                else:
                    return self.patch > other.patch
            else:
                return self.minor > other.minor
        else:
            return self.major > other.major

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


def _test_version(executable: Union[bytes, str, os.PathLike]) -> _SemverVersion:
    call = subprocess.run([executable, "-version"], capture_output=True)
    match = FFMPEG_RE.match(call.stdout.decode("utf-8"))
    return _SemverVersion(match.group("version"))


def _download_binaries(json_data: _BinariesJSON) -> None:
    package_folder = pathlib.Path(__file__).parent.parent.parent
    binaries_folder = package_folder.joinpath("binaries")
    if binaries_folder.exists():
        shutil.rmtree(binaries_folder)
    os.mkdir(binaries_folder)

    version = _SemverVersion(json_data["version"])
    downloader: _Downloader
    platform = sys.platform
    if platform in ["win32", "cygwin"]:
        downloader = _WinDownloader(json_data["url"]["win"], binaries_folder)
    elif platform == "darwin":
        downloader = _MacDownloader(json_data["url"]["mac"], binaries_folder)
    elif platform == "linux":
        downloader = _NixDownloader(json_data["url"]["nix"], binaries_folder)
    else:
        raise RuntimeError(f"Binaries for platform {platform} not supported")
    downloader.run()
    downloaded_version = _test_version(downloader.ffmpeg)
    if downloaded_version != version:
        raise RuntimeError(f"Expected version {version}. Got {downloaded_version}")


def download_binaries() -> None:
    json_file_path = pathlib.Path(__file__).parent.joinpath("binaries.json")
    with open(json_file_path) as json_file:
        json_content = json.load(json_file)
    _download_binaries(json_content)


def get_binaries() -> Union[Tuple[pathlib.Path, pathlib.Path], None]:
    package_folder = pathlib.Path(__file__).parent.parent.parent
    binaries_folder = package_folder.joinpath("binaries")
    platform = sys.platform
    if platform in ["win32", "cygwin"]:
        downloader = _WinDownloader([], binaries_folder)
    elif platform == "darwin":
        downloader = _MacDownloader([], binaries_folder)
    elif platform == "linux":
        downloader = _NixDownloader([], binaries_folder)
    else:
        raise RuntimeError(f"Binaries for platform {platform} not supported")
    candidate_bin = pathlib.Path(downloader.ffmpeg)
    candidate_probe = pathlib.Path(downloader.ffprobe)
    if (
        candidate_bin.exists()
        and candidate_bin.is_file()
        and candidate_probe.exists()
        and candidate_probe.is_file()
    ):
        return candidate_bin, candidate_probe
    return None
