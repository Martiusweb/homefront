# coding: utf-8
from typing import Any, Dict, Optional, Union

import os.path

import pelican

#: Subdirectory in which homefront store its cached data
CACHE_SUBDIR = "_homefront"

DEFAULT_SETTINGS = {
    #: Bootstrap version to use, unless overriden in settings
    "BOOTSTRAP_VERSION": "4.3",
    #: Sass source pattern: files matching this pattern in the base path will
    #: be compiled with Sass.
    "SASS_SOURCE_PATTERN": "scss/[!_]*.scss",
    #: Sass include path, as an iterable of path
    "SASS_INCLUDE_PATH": ("scss/vendor", ),
    #: Sass output path (relative to the output directory of pelican)
    "SASS_OUTPUT_PATH": "css",
}


Settings = Dict[str, Any]


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
