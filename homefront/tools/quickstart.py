# coding: utf-8
"""
Wraps and extends the pelican-quickstart tool to create directories for Sass
(CSS) and Javascript sources.
"""
import os.path
import shutil

import pkg_resources

import pelican
import pelican.tools.pelican_quickstart

import homefront.bootstrap
import homefront.settings


#: Default theme from homefront
_DEFAULT_THEME = "themes/default"


def main():
    pelican.tools.pelican_quickstart.main()
    pelican_qs_conf = pelican.tools.pelican_quickstart.CONF
    base_dir = pelican_qs_conf['basedir']
    theme_dir = os.path.join(base_dir, _DEFAULT_THEME)

    settings_filename = os.path.join(base_dir, pelican.DEFAULT_CONFIG_NAME)

    print("Creating Homefront project")

    # We load settings before updating theme because they may not load until
    # the project is created
    try:
        settings = pelican.read_settings(settings_filename)
        homefront.settings.update(settings)
    except (homefront.Error, OSError) as error:
        print(f"Error: {error}")

    try:
        with open(settings_filename, "a") as settings_file:
            settings_file.write(
                "\n\n# Plugins\n"
                "PLUGINS = ('homefront.pelican.bootstrap', )\n"
                f"THEME = '{theme_dir}'")
    except (homefront.Error, OSError) as error:
        print(f"Error: {error}")

    try:
        theme_source_dir = pkg_resources.resource_filename(
            "homefront", _DEFAULT_THEME)
        shutil.copytree(theme_source_dir, theme_dir)
    except (homefront.Error, OSError) as error:
        print(f"Error: {error}")

    try:
        version = settings["BOOTSTRAP_VERSION"]
        print(f"Downloading bootstrap {version}")

        cachedir = homefront.settings.get_cache_dir(settings, base_dir)
        os.makedirs(cachedir, exist_ok=True)

        bootstrap_dir = os.path.join(cachedir, f"bootstrap-{version}")
        homefront.bootstrap.download_bootstrap(version, bootstrap_dir)

        for filename in ("_variables.scss", ):
            shutil.copy(
                os.path.join(bootstrap_dir, "scss", "bootstrap", filename),
                os.path.join(theme_dir, "scss", filename))
    except (homefront.Error, OSError) as error:
        print(f"Error: {error}")

    try:
        # Add a .gitignore
        with open(os.path.join(base_dir, ".gitignore"), "a") as gitignore:
            gitignore.write(
                "\n# Added by homefront\n"
                "__pycache__\n"
            )

            for ignored in ("CACHE_PATH", "OUTPUT_PATH", ):
                ignored = settings[ignored].rstrip(os.path.sep) + os.path.sep
                gitignore.write(f"{ignored}\n")
    except (homefront.Error, OSError) as error:
        print(f"Error: {error}")

    print("Done, homefront project structure created")
    print(f"You can customize the theme in {theme_dir}")
