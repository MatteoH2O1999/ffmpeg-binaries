import os
import pathlib
import tempfile
import requests
import patoolib
import shutil

from typing import Union
from .downloader import Downloader


class WinDownloader(Downloader):
    def run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            for link in self.url:
                filename = link.split("/")[-1]
                filepath = pathlib.Path(tmp_dir).joinpath(filename)
                print(f"Downloading {link} to file {filepath}...")
                response = requests.get(link)
                with open(filepath, 'wb') as file:
                    file.write(response.content)
                print(f"Extracting archive {filepath} to {self.dst}...")
                patoolib.extract_archive(str(filepath), outdir=self.dst)
        directories = os.listdir(self.dst)
        if len(directories) != 1:
            raise RuntimeError(f"Only 1 directory should be extracted. Got {len(directories)}")
        directory = pathlib.Path(self.dst).joinpath(directories[0])
        for path in os.listdir(directory):
            complete_file = directory.joinpath(path)
            shutil.copy2(complete_file, self.dst)
            print(f"Copied {complete_file} to {self.dst}")
        print(f"Extracted content from {directory} to {self.dst}")
        shutil.rmtree(directory)
        print(f"Removed {directory}")

    @property
    def ffmpeg(self) -> Union[bytes, str, os.PathLike]:
        return pathlib.Path(self.dst).joinpath("bin").joinpath("ffmpeg.exe")
