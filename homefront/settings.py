# coding: utf-8
from typing import Dict, Optional, Union

import os.path

import pelican

#: Subdirectory in which homefront store its cached data
CACHE_SUBDIR = "_homefront/"


def pelican_settings(basedir: str, config_name: Optional[str] = None) -> Dict:
    """
    Read settings for the pelican settup at the given location.

    :param basedir: pelican website installation
    :param config_name: name of the config file under ``basedir``
    """
    settings_filename = os.path.join(
        basedir, config_name or pelican.DEFAULT_CONFIG_NAME)

    return pelican.read_settings(settings_filename)


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
