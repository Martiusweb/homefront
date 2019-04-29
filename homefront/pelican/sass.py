# coding: utf-8
from typing import Type

import glob
import itertools
import logging
import os.path

import pelican
import pelican.signals
import sass

import homefront.generators

LOG = logging.getLogger(__name__)

_DEFAULT_OUTPUT_STYLE = "nested"


class SassGenerator(homefront.generators.Generator):  # pylint: disable=R0903
    """
    Compile and minify sass files and move them to a static folder.

    Sources are looked into the directory of the activated theme, under
    ``SASS_SOURCE_PATTERN``.

    Does nothing unless configured, it is not required to include this plugin
    when using ``homefront.bootstrap``.
    """
    sources = []
    include_path = []

    def generate_output(self, _) -> None:
        sass_output_path = os.path.join(
            self.output_path,
            self.settings["THEME_STATIC_DIR"],
            self.settings["SASS_OUTPUT_PATH"])

        include_path = list(itertools.chain(
            self.include_path, self.settings["SASS_INCLUDE_PATH"]))

        LOG.debug("Sass include_path is: %s", include_path)

        # Find files from configuration, use glob to list files
        pattern = os.path.join(self.settings["THEME"],
                               self.settings["SASS_SOURCE_PATTERN"])
        sources = itertools.chain(self.sources, glob.iglob(pattern))

        os.makedirs(sass_output_path, exist_ok=True)

        LOG.debug("Sass compiler is looking for %s", pattern)

        source_map_args = {}
        if self.settings["SASS_GENERATE_SOURCE_MAP"]:
            source_map_args["source_comments"] = True

        for source in sources:
            destname = os.path.splitext(os.path.basename(source))[0]

            LOG.info("Compiling %s to %s",
                     source,
                     os.path.join(sass_output_path, destname) + ".css")

            if source_map_args:
                source_map_args["source_map_filename"] = os.path.join(
                    sass_output_path,
                    destname + ".css.map")

            css = sass.compile(
                filename=source,
                output_style=self.settings["SASS_OUTPUT_STYLE"],
                include_paths=include_path,
                **source_map_args)

            if source_map_args:
                css, source_map = css

            dest = os.path.join(sass_output_path, destname)

            with open(dest + ".css", "w") as css_file:
                css_file.write(css)

            if source_map_args:
                with open(dest + ".css.map", "w") as css_file:
                    css_file.write(source_map)


def get_generators(_: pelican.Pelican) -> Type[SassGenerator]:
    """
    Return the class of the generator implemented by this plugin.
    """
    return SassGenerator


def register():
    """
    Register pelican signal handlers.
    """
    pelican.signals.get_generators.connect(get_generators)
