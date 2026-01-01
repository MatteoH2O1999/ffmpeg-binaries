import logging
import os
import pathlib
import shutil

from typing import Union
from .downloader import _Downloader


logger = logging.getLogger(__name__)


class _WinDownloader(_Downloader):
    def extract(self) -> None:
        directories = os.listdir(self.dst)
        if len(directories) != 1:
            raise RuntimeError(
                f"Only 1 directory should be extracted. Got {len(directories)}"
            )
        directory = pathlib.Path(self.dst).joinpath(directories[0])
        for path in os.listdir(directory):
            complete_file = directory.joinpath(path)
            shutil.move(complete_file, self.dst)
            logger.info(f"Moved {complete_file} to {self.dst}")
        logger.info(f"Extracted content from {directory} to {self.dst}")
        shutil.rmtree(directory)
        logger.info(f"Removed {directory}")

    @property
    def ffmpeg(self) -> Union[bytes, str, os.PathLike]:
        return pathlib.Path(self.dst).joinpath("bin").joinpath("ffmpeg.exe")

    @property
    def ffprobe(self) -> Union[bytes, str, os.PathLike]:
        return pathlib.Path(self.dst).joinpath("bin").joinpath("ffprobe.exe")
