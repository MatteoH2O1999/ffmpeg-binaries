import pytest

import ffmpeg.internals.downloaders.binaries_downloader as internals


def test_semver_parsing_success():
    parsed_complete = internals._SemverVersion("3.2.1")
    parsed_minor = internals._SemverVersion("3.2")
    parsed_major = internals._SemverVersion("3")

    assert parsed_complete.major == 3
    assert parsed_complete.minor == 2
    assert parsed_complete.patch == 1

    assert parsed_minor.major == 3
    assert parsed_minor.minor == 2
    assert parsed_minor.patch == 0

    assert parsed_major.major == 3
    assert parsed_major.minor == 0
    assert parsed_major.patch == 0


def test_semver_parsing_failed():
    with pytest.raises(ValueError):
        internals._SemverVersion("")
    with pytest.raises(ValueError):
        internals._SemverVersion("a")
