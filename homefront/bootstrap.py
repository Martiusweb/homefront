# coding: utf-8
from typing import List, Union

import dataclasses
import os

import homefront
import homefront.googleclosure
import homefront.release


class Bootstrap(homefront.release.NpmRelease):
    """
    Represents a release to fetch.
    """
    def __init__(self, required_version: str,
                 destination: Union[str, os.PathLike]):
        super().__init__(required_version, "bootstrap", destination, {
            # scss files are under a bootstrap directory, so they can be
            # included with "bootstrap/the_lib".
            "package/scss/": "scss/bootstrap",
            # js files are compressed and concatenated anyway.
            "package/js/src/": "js/",
            "package/package.json": "package.json"
        })


def download(version: str, destination: Union[str, os.PathLike]) -> None:
    release = Bootstrap(version, destination)
    release.install()

    for dep in release.get_dependencies():
        dep.install()


@dataclasses.dataclass
class ArtifactWithBootstrap(homefront.googleclosure.Artifact):
    """
    Extended artifact which includes bootstrap sources.
    """
    bootstrap_modules: List[str] = dataclasses.field(default_factory=list)
    bootstrap_path: Union[str, os.PathLike] = ""
    dependencies_path: Union[str, os.PathLike] = ""

    @classmethod
    def from_artifact(cls, artifact: homefront.googleclosure.Artifact
                      ) -> 'ArtifactWithBootstrap':
        return cls(artifact.output_name, artifact.sources, artifact.externs,
                   artifact.compilation_level)

    def resolve_sources(self, basedir: Union[str, os.PathLike]):
        for module in self.bootstrap_modules:
            yield os.path.join(self.bootstrap_path, module + ".js")

        # Add dependencies
        yield os.path.join(self.dependencies_path, "**/package.json")
        yield os.path.join(self.dependencies_path, "**.js")

        yield from super().resolve_sources(basedir)


def bootstrapify(artifact: homefront.googleclosure.Artifact,
                 *modules: List[str]):
    """
    Add boostrap ``modules`` to a Google Closure Compiler artifact.

    By default, all modules are added.
    """
    result = ArtifactWithBootstrap.from_artifact(artifact)
    result.bootstrap_modules = modules
    return result
