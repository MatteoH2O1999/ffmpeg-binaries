import os

from abc import ABC, abstractmethod
from typing import Union


class Downloader(ABC):
    def __init__(self, url: list[str], dst: Union[bytes, str, os.PathLike]):
        self.url = url
        self.dst = dst

    @abstractmethod
    def run(self) -> None:
        pass

    @property
    @abstractmethod
    def ffmpeg(self) -> Union[bytes, str, os.PathLike]:
        pass
