# coding: utf-8
from typing import List, Union

import dataclasses
import enum
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


class CompilationLevel(enum.Enum):
    WHITESPACE_ONLY = 0
    SIMPLE_OPTIMIZATIONS = 1
    ADVANCED_OPTIMIZATIONS = 2

    def __str__(self):
        return self.name


@dataclasses.dataclass
class Artifact:
    # pylint: disable=R0903
    output_name: str
    sources: List[str]
    externs: List[str] = dataclasses.field(default_factory=list)
    compilation_level: CompilationLevel = CompilationLevel.SIMPLE_OPTIMIZATIONS

    def resolve_sources(self, basedir: Union[str, os.PathLike]):
        for source in self.sources:
            yield os.path.join(basedir, source)

    def resolve_externs(self, basedir: Union[str, os.PathLike]):
        for extern in self.externs:
            yield os.path.join(basedir, extern)
