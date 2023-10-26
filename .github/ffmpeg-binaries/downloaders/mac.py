import os
import pathlib

from typing import Union
from .downloader import Downloader


class MacDownloader(Downloader):
    def run(self) -> None:
        print(f"{self.url}, {self.dst}")

    @property
    def ffmpeg(self) -> Union[bytes, str, os.PathLike]:
        return pathlib.Path(self.dst).joinpath("ffmpeg")
