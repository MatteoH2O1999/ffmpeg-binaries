import os
import shutil
import subprocess
import sys
import pathlib

from typing import TypedDict, Union
from .downloader import Downloader
from .mac import MacDownloader
from .nix import NixDownloader
from .win import WinDownloader


class BinariesURL(TypedDict):
    win: list[str]
    nix: list[str]
    mac: list[str]


class BinariesJSON(TypedDict):
    version: str
    url: BinariesURL


class SemverVersion:
    def __init__(self, string_version: str):
        split_version = string_version.split(".")
        while len(split_version) != 3:
            split_version.append('0')

        self.major = int(split_version[0])
        self.minor = int(split_version[1])
        self.patch = int(split_version[2])

    def __eq__(self, other):
        if not isinstance(other, SemverVersion):
            return False
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


def test_version(executable: Union[bytes, str, os.PathLike]) -> SemverVersion:
    call = subprocess.run([executable, '--version'], capture_output=True)
    raise NotImplementedError


def download_binaries(json_data: BinariesJSON) -> None:
    root = pathlib.Path(__file__).parent.parent.parent.parent
    src_folder = root.joinpath("src")
    package_folder = src_folder.joinpath("ffmpeg")
    binaries_folder = package_folder.joinpath("binaries")
    if binaries_folder.exists():
        shutil.rmtree(binaries_folder)
    os.mkdir(binaries_folder)

    version = SemverVersion(json_data['version'])
    downloader: Downloader
    platform = sys.platform
    if platform in ['win32', 'cygwin']:
        downloader = WinDownloader(json_data['url']['win'], binaries_folder)
    elif platform == 'darwin':
        downloader = MacDownloader(json_data['url']['mac'], binaries_folder)
    elif platform == 'linux':
        downloader = NixDownloader(json_data['url']['nix'], binaries_folder)
    else:
        raise RuntimeError(f"Binaries for platform {platform} not supported")
    downloader.run()
    downloaded_version = test_version(downloader.ffmpeg)
    if downloaded_version != version:
        raise RuntimeError(f"Expected version {version}. Got {downloaded_version}")
