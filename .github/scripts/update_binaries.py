import json
import git
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
        print("Downloading ffmpeg repo...")
        python_repo = git.Repo.clone_from("https://git.ffmpeg.org/ffmpeg.git", temp_dir)
        repo_tags = python_repo.tags
        print("Extracting tags...")
        for tag in repo_tags:
            tag = tag.name.replace("n", "")
            try:
                semantic_tags.append(_SemverVersion(tag))
            except ValueError:
                pass
    print("Sorting tags...")
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
    for tag in ffmpeg_tags:
        tag = _SemverVersion(tag)
        if tag <= current_best:
            print(
                f"Already reached latest version with tag {tag}. Stopping...",
                flush=True,
            )
            return
        print(f"::group::Trying with tag {tag}", flush=True)
        candidate = try_version(tag)
        print("::endgroup::", flush=True)
        if candidate is not None and tag > current_best:
            current_url = candidate
            current_best = tag
    new_binaries_json: _BinariesJSON = {
        "version": str(current_best),
        "url": current_url,
    }
    with open(json_path, "w") as json_file:
        json.dump(new_binaries_json, json_file, indent=2)


def try_version(version: _SemverVersion) -> Union[None, _BinariesURL]:
    patch_dict = get_urls(f"{version.major}.{version.minor}.{version.patch}")
    minor_dict = get_urls(f"{version.major}.{version.minor}")
    major_dict = get_urls(f"{version.major}")
    if try_url(patch_dict):
        return patch_dict
    if try_url(minor_dict):
        return minor_dict
    if try_url(major_dict):
        return major_dict


def get_urls(version: str) -> _BinariesURL:
    return {
        "win": [
            f"https://github.com/GyanD/codexffmpeg/releases/download/{version}/ffmpeg-{version}-essentials_build.7z"
        ],
        "mac": [
            f"https://evermeet.cx/ffmpeg/ffmpeg-{version}.7z",
            f"https://evermeet.cx/ffmpeg/ffprobe-{version}.7z",
        ],
        "nix": [
            f"https://www.johnvansickle.com/ffmpeg/old-releases/ffmpeg-{version}-amd64-static.tar.xz"
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


if __name__ == "__main__":
    update_binaries(gather_tags())
