import os
import pathlib

from typing import Union
from .downloader import _Downloader


class _MacDownloader(_Downloader):
    def extract(self) -> None:
        pass

    @property
    def ffmpeg(self) -> Union[bytes, str, os.PathLike]:
        return pathlib.Path(self.dst).joinpath("ffmpeg")
