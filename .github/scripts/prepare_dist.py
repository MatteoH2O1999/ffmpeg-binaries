import os
import pathlib
import shutil


def extract_content(directory, dist_folder):
    for path in os.listdir(directory):
        complete_file = directory.joinpath(path)
        shutil.move(complete_file, dist_folder)
        print(f"Moved {complete_file} to {dist_folder}", flush=True)
    print(f"Extracted content from {directory} to {dist_folder}", flush=True)
    shutil.rmtree(directory)
    print(f"Removed {directory}", flush=True)


if __name__ == "__main__":
    root = pathlib.Path(__file__).parent.parent.parent
    dist = root.joinpath("dist")
    for entry in os.listdir(dist):
        complete_path = dist.joinpath(entry)
        if complete_path.is_dir():
            extract_content(complete_path, dist)
