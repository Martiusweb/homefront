# coding: utf-8
from typing import Union

import os

import homefront
import homefront.release


class Release(homefront.release.NpmRelease):
    """
    Represents a release to fetch.
    """
    def __init__(self, required_version: str,
                 destination: Union[str, os.PathLike]):
        super().__init__(
            required_version, "bootstrap", destination,
            # scss files are under a bootstrap directory, so they can be
            # included with "bootstrap/thelib".
            {"package/scss/": "scss/bootstrap"}
        )
        self.name = "Bootstrap"


def download(version: str, destination: Union[str, os.PathLike]) -> None:
    release = Release(version, destination)
    release.install()
