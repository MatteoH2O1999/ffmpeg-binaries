import logging
from ffmpeg.internals import download_binaries


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    download_binaries()
