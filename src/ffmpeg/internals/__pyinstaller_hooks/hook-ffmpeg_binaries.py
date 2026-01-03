import os
from PyInstaller.utils.hooks import collect_data_files

if "ffmpeg_binaries" in __file__.split(os.sep):
    datas = collect_data_files("ffmpeg_binaries")
