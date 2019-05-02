# coding: utf-8
from typing import Any, Dict, Optional, Union

import os.path

import pelican

from homefront.bootstrap import bootstrapify
from homefront.googleclosure import Artifact

Settings = Dict[str, Any]

#: Subdirectory in which homefront store its cached data
CACHE_SUBDIR = "_homefront"

DEFAULT_SETTINGS: Settings = {
    #: Bootstrap version to use, unless overriden in settings
    "BOOTSTRAP_VERSION": "4.3",
    #: Generate a boostrap Javascript artifact, the first argument is a
    #: (possibly empty) artifact on which the boostrap modules are added.
    "BOOTSTRAP_JS_ARTIFACT": bootstrapify(Artifact("bootstrap.js", []), "*"),

    #: Sass source pattern: files matching this pattern in the base path will
    #: be compiled with Sass.
    "SASS_SOURCE_PATTERN": "scss/[!_]*.scss",
    #: Sass include path, as an iterable of path
    "SASS_INCLUDE_PATH": ("scss/vendor", ),
    #: Sass output path (relative to ``THEME_STATIC_DIR``)
    "SASS_OUTPUT_PATH": "css",
    #: Sass output style, one of 'nested', 'expanded', 'compact', 'compressed'
    "SASS_OUTPUT_STYLE": "compressed",
    #: Sass source maps generation
    "SASS_GENERATE_SOURCE_MAP": True,

    #: Google Closure Compiler version to use
    "GOOGLE_CLOSURE_COMPILER_VERSION": "20190301.0.0",
    #: Google Closure Compiler version to use
    "GOOGLE_CLOSURE_COMPILER_OUTPUT_PATH": "js",
    #: Google Closure Compiler artifacts as a list of googleclosure.Artifact:
    #: For instance::
    #:
    #:     homefront.googleclosure.Artifact(
    #:         "main.js", ["js/*.js", "js/vendor/*.js]
    #:     )
    #:
    #: There are a few more options for cases where one want to use advanced
    #: optimizations.
    "GOOGLE_CLOSURE_COMPILER_ARTIFACTS": [
        Artifact("main.js", ("js/*.js", )),
    ],
}


def update(settings: Settings) -> None:
    """
    Update ``settings`` to defined undefined settings to their defaults.

    :param settings: pelican settings dict
    """
    if "_homefront_settings_loaded" not in settings:
        settings["_homefront_settings_loaded"] = True
        for name, default in DEFAULT_SETTINGS.items():
            if name not in settings:
                settings[name] = default


def read_pelican_settings(basedir: str, config_name: Optional[str] = None
                          ) -> Settings:
    """
    Read settings for the pelican settup at the given location, injects
    homefront settings.

    :param basedir: pelican website installation
    :param config_name: name of the config file under ``basedir``
    """
    settings_filename = os.path.join(
        basedir, config_name or pelican.DEFAULT_CONFIG_NAME)

    settings = pelican.read_settings(settings_filename)
    update(settings)
    return settings


def get_cache_dir(settings: Union[str, Dict], basedir: str = "") -> str:
    """
    Return the path to homefront cache.

    :param settings: the patch to the pelican cache, or pelican settings dict
    :param basedir: optional pelication website installation dir
    """
    if isinstance(settings, str):
        cachedir = settings
    else:
        cachedir = settings["CACHE_PATH"]

    return os.path.join(basedir, cachedir, CACHE_SUBDIR)
