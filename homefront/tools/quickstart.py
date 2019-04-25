# coding: utf-8
"""
Wraps and extends the pelican-quickstart tool to create directories for Sass
(CSS) and Javascript sources.
"""
import os.path

import homefront.settings

import pelican
import pelican.tools.pelican_quickstart


def main():
    pelican.tools.pelican_quickstart.main()
    pelican_qs_conf = pelican.tools.pelican_quickstart.CONF
    basedir = pelican_qs_conf['basedir']

    settings_filename = os.path.join(basedir, pelican.DEFAULT_CONFIG_NAME)
    settings = pelican.read_settings(settings_filename)

    try:
        for subdir in ("scss", "js"):
            os.makedirs(os.path.join(basedir, subdir), exist_ok=True)

        cachedir = homefront.settings.get_cache_dir(settings, basedir)
        os.makedirs(cachedir, exist_ok=True)
    except (homefront.Error, OSError) as error:
        print(f"Error: {error}")

    with open(os.path.join(basedir, ".gitignore"), "a") as gitignore:
        gitignore.write(
            "\n# Added by homefront\n"
            "__pycache__\n"
        )

        for ignored in ("CACHE_PATH", "OUTPUT_PATH", ):
            ignored = settings[ignored].rstrip(os.path.sep) + os.path.sep
            gitignore.write(f"{ignored}\n")

    # TODO add homefront plugins
    # TODO checkout bootstrap (download the tarball)
