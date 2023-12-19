import os
import tempfile
import pathlib
import patoolib
import requests

from abc import ABC, abstractmethod
from typing import List, Union


class _Downloader(ABC):
    def __init__(self, url: List[str], dst: Union[bytes, str, os.PathLike]):
        self.url = url
        self.dst: pathlib.Path = pathlib.Path(dst)

    def run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            for link in self.url:
                filename = link.split("/")[-1]
                filepath = pathlib.Path(tmp_dir).joinpath(filename)
                print(f"Downloading {link} to file {filepath}...", flush=True)
                response = requests.get(link)
                with open(filepath, "wb") as file:
                    file.write(response.content)
                print(f"Extracting archive {filepath} to {self.dst}...", flush=True)
                patoolib.extract_archive(str(filepath), outdir=str(self.dst))
        self.extract()

    @abstractmethod
    def extract(self) -> None:
        pass

    @property
    @abstractmethod
    def ffmpeg(self) -> Union[bytes, str, os.PathLike]:
        pass

    @property
    @abstractmethod
    def ffprobe(self) -> Union[bytes, str, os.PathLike]:
        pass
