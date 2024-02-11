import json
import git
import os
import pathlib
import requests
import tempfile
import time

from typing import List, Union

from ffmpeg.internals.downloaders.binaries_downloader import (
    _BinariesJSON,
    _BinariesURL,
    _SemverVersion,
)


def gather_tags() -> List[str]:
    tags = []
    semantic_tags: List[_SemverVersion] = []
    with tempfile.TemporaryDirectory() as temp_dir:
        print("Downloading ffmpeg repo...", flush=True)
        python_repo = git.Repo.clone_from("https://git.ffmpeg.org/ffmpeg.git", temp_dir)
        repo_tags = python_repo.tags
        print("Extracting tags...", flush=True)
        for tag in repo_tags:
            tag = tag.name.replace("n", "")
            try:
                semantic_tags.append(_SemverVersion(tag))
            except ValueError:
                pass
    print("Sorting tags...", flush=True)
    semantic_tags.sort(reverse=True)
    for t in semantic_tags:
        tags.append(str(t))
    return tags


def update_binaries(ffmpeg_tags: List[str]):
    json_path = (
        pathlib.Path(__file__)
        .parent.parent.parent.joinpath("src")
        .joinpath("ffmpeg")
        .joinpath("internals")
        .joinpath("downloaders")
        .joinpath("binaries.json")
    )
    with open(json_path) as json_file:
        binaries: _BinariesJSON = json.load(json_file)
        version: _SemverVersion = _SemverVersion(binaries["version"])
    print(f"Current version: {version}", flush=True)
    print(f"Current binaries:\n{json.dumps(binaries['url'], indent=2)}\n", flush=True)
    current_best = version
    current_url = binaries["url"]
    set_output("OLD", str(current_best))
    for tag in ffmpeg_tags:
        tag = _SemverVersion(tag)
        if tag <= current_best:
            print(
                f"Already reached latest version with tag {tag}. Stopping...",
                flush=True,
            )
            set_output("NEW", str(current_best))
            return
        print(f"::group::Trying with tag {tag}", flush=True)
        candidate = try_version(tag)
        print("::endgroup::", flush=True)
        if candidate is not None and tag > current_best:
            current_url = candidate
            current_best = tag
            break
    new_binaries_json: _BinariesJSON = {
        "version": str(current_best),
        "url": current_url,
    }
    print(f"New version: {current_best}", flush=True)
    set_output("NEW", str(current_best))
    with open(json_path, "w") as json_file:
        json.dump(new_binaries_json, json_file, indent=2)


def try_version(version: _SemverVersion) -> Union[None, _BinariesURL]:
    patch_dict = get_urls(f"{version.major}.{version.minor}.{version.patch}")
    minor_dict = get_urls(f"{version.major}.{version.minor}")
    major_dict = get_urls(f"{version.major}")
    if try_url(patch_dict):
        return patch_dict
    if version.patch != 0:
        return None
    if try_url(minor_dict):
        return minor_dict
    if version.minor != 0:
        return None
    if try_url(major_dict):
        return major_dict
    return None


def get_urls(version: str) -> _BinariesURL:
    return {
        "win": [
            f"https://github.com/GyanD/codexffmpeg/releases/download/{version}/ffmpeg-{version}-essentials_build.7z"
        ],
        "nix": [
            f"https://www.johnvansickle.com/ffmpeg/old-releases/ffmpeg-{version}-amd64-static.tar.xz"
        ],
        "mac": [
            f"https://evermeet.cx/ffmpeg/ffmpeg-{version}.7z",
            f"https://evermeet.cx/ffmpeg/ffprobe-{version}.7z",
        ],
    }


def try_url(urls: _BinariesURL) -> bool:
    print(f"Trying binaries:\n{json.dumps(urls, indent=2)}", flush=True)
    url_list = [*urls["nix"], *urls["win"], *urls["mac"]]
    for url in url_list:
        print(f"Checking url: {url}", flush=True)
        success = False
        retries = 3
        while retries and not success:
            response = requests.get(url, timeout=None)
            if response.ok:
                success = True
                print("Success.")
            elif response.status_code == 404:
                retries = 0
            else:
                time.sleep(2 ** ((4 - retries) * 2))
                retries -= 1
        if not success:
            print("Failed.")
            return False
    return True


def set_output(name, output):
    file_path = os.environ.get("GITHUB_OUTPUT", "")
    if not file_path:
        raise ValueError
    with open(file_path, "a") as file:
        file.write(f"{name}={output}\n")


if __name__ == "__main__":
    update_binaries(gather_tags())
