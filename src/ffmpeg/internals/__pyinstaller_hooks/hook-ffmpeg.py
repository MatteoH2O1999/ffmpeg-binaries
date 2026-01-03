import os
from PyInstaller.utils.hooks import collect_data_files

if "ffmpeg_binaries" not in __file__.split(os.sep):
    datas = collect_data_files("ffmpeg")
