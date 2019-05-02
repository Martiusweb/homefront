# coding: utf-8
from typing import List, Type

import glob
import itertools
import logging
import os.path
import subprocess

import pelican
import pelican.signals

import homefront.generators
import homefront.googleclosure

LOG = logging.getLogger(__name__)


def _globs(patterns):
    patterns = list(patterns)
    print("plop", patterns)
    return itertools.chain.from_iterable(map(glob.iglob, patterns))


class GoogleClosureGenerator(homefront.generators.Generator):
    # pylint: disable=R0903
    """
    Compile and minify javascript file with Google Closure Compiler.
    """
    artifacts: List[homefront.googleclosure.Artifact] = []

    def generate_output(self, _) -> None:
        artifacts = itertools.chain(
            self.artifacts, self.settings["GOOGLE_CLOSURE_COMPILER_ARTIFACTS"])

        output_dir = os.path.join(
            self.output_path,
            self.settings["THEME_STATIC_DIR"],
            self.settings["GOOGLE_CLOSURE_COMPILER_OUTPUT_PATH"])

        for artifact in artifacts:
            sources = _globs(artifact.resolve_sources(self.settings["THEME"]))
            externs = _globs(artifact.resolve_externs(self.settings["THEME"]))

            self.compile(os.path.join(output_dir, artifact.output_name),
                         sources, externs, artifact.compilation_level)

    def get_compiler_filename(self) -> str:
        version = self.settings["GOOGLE_CLOSURE_COMPILER_VERSION"]
        install_dir = os.path.join(
            homefront.settings.get_cache_dir(self.settings),
            f"googleclosure-{version}")
        filename = os.path.join(install_dir,  "compiler")

        if not os.path.exists(filename):
            LOG.debug("Installing Google Closure Compiler")
            homefront.googleclosure.download(version, install_dir)

        return filename

    def compile(self, output_name: str, sources: List[str],
                externs: List[str] = tuple(),
                compilation_level: homefront.googleclosure.CompilationLevel
                = homefront.googleclosure.CompilationLevel.SIMPLE_OPTIMIZATIONS
                ) -> None:
        cli = [self.get_compiler_filename(),
               "--compilation_level", str(compilation_level),
               "--js_output_file", output_name]

        source = None
        for source in sources:
            cli.extend(("--js", source))

        if not source:
            LOG.debug("No source files for artifact %s", output_name)
            return

        for extern in externs:
            cli.extend(("--externs", extern))

        try:
            subprocess.run(cli, check=True, capture_output=True)
        except subprocess.CalledProcessError as exc:
            LOG.error("Google Closure Compiler failed with error:\n%s",
                      exc.stderr)


def get_generators(_: pelican.Pelican) -> Type[GoogleClosureGenerator]:
    """
    Return the class of the generator implemented by this plugin.
    """
    return GoogleClosureGenerator


def register():
    """
    Register pelican signal handlers.
    """
    pelican.signals.get_generators.connect(get_generators)
