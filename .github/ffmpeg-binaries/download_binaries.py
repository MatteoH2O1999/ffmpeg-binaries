import json
import pathlib

from downloaders.binaries_downloader import download_binaries


if __name__ == "__main__":
    with open(pathlib.Path(__file__).parent.joinpath("binaries.json")) as json_file:
        data = json.load(json_file)
    download_binaries(data)
