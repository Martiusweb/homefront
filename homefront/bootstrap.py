# coding: utf-8
from typing import Union

import os

import homefront
import homefront.release

_GITHUB_BOOTSTRAP_REPO = "twbs/bootstrap"

_ARCHIVE_DIRECTORIES_TO_EXTRACT = {
    "*bootstrap-*/scss/": "scss/bootstrap",
    "*bootstrap-*/js/src/": "js/bootstrap",
}


class Release(homefront.release.GithubRelease):
    """
    Represents a release to fetch from github.
    """
    def __init__(self, required_version: str,
                 destination: Union[str, os.PathLike]):
        super().__init__(required_version, _GITHUB_BOOTSTRAP_REPO, destination,
                         _ARCHIVE_DIRECTORIES_TO_EXTRACT)
        self.name = "Bootstrap"


def download(version: str, destination: Union[str, os.PathLike]) -> None:
    release = Release(version, destination)
    release.install()
