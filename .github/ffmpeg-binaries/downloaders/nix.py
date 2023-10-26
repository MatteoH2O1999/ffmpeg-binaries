import os
import pathlib
import shutil

from typing import Union
from .downloader import Downloader


class NixDownloader(Downloader):
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
            print(f"Moved {complete_file} to {self.dst}", flush=True)
        print(f"Extracted content from {directory} to {self.dst}", flush=True)
        shutil.rmtree(directory)
        print(f"Removed {directory}", flush=True)

    @property
    def ffmpeg(self) -> Union[bytes, str, os.PathLike]:
        return pathlib.Path(self.dst).joinpath("ffmpeg")
