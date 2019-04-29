# coding: utf-8

from typing import Union

import os
import sys

import homefront
import homefront.release


_PACKAGE = {
    "linux": "google-closure-compiler-linux",
    "darwin": "google-closure-compiler-osx",
}

_ARCHIVE_DIRECTORIES_TO_EXTRACT = {
    "package/compiler": "",
}


class Release(homefront.release.NpmRelease):
    def __init__(self, required_version: str,
                 destination: Union[str, os.PathLike]):
        if sys.platform not in _PACKAGE:
            raise homefront.Error(
                "Unsupported platform for google closure compiler")

        super().__init__(required_version, _PACKAGE[sys.platform],
                         destination, _ARCHIVE_DIRECTORIES_TO_EXTRACT)
        self.name = "Google closure compiler"


def download(version: str, destination: Union[str, os.PathLike]) -> None:
    """
    Installs closure native.
    """
    release = Release(version, destination)
    release.install()
