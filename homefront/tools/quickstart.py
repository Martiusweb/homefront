# coding: utf-8
"""
Wraps and extends the pelican-quickstart tool to create directories for Sass
(CSS) and Javascript sources.
"""
from typing import Dict

import datetime
import json
import os
import shutil
import sys

import pkg_resources

import pelican
import pelican.tools.pelican_quickstart

import homefront.bootstrap
import homefront.settings


#: Default theme from homefront
_DEFAULT_THEME = "themes/default"


def step(func, desc=None, details=None):
    if desc:
        print(desc)
    elif details:
        print(func.__doc__ + " " + details)
    else:
        print(func.__doc__)

    try:
        return func()
    except (homefront.Error, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)


def pelican_quickstart() -> str:
    """
    Runs pelican-quickstart
    """
    pelican.tools.pelican_quickstart.main()
    pelican_qs_conf = pelican.tools.pelican_quickstart.CONF
    return pelican_qs_conf['basedir']


class Website:
    def __init__(self, base_dir: str):
        self.base_dir: str = base_dir
        self.theme_dir: str = os.path.join(base_dir, _DEFAULT_THEME)
        self.settings_filename: str = os.path.join(
            base_dir, pelican.DEFAULT_CONFIG_NAME)

        # We load settings before updating theme because they may not load
        # until the project is created
        self.settings: Dict = pelican.read_settings(self.settings_filename)
        homefront.settings.update(self.settings)

    def update_settings(self) -> None:
        """Updating the settings file"""
        with open(self.settings_filename, "a") as settings_file:
            settings_file.write(
                "\n\n# Plugins\n"
                "PLUGINS = ('homefront.pelican.bootstrap', )\n"
                f"THEME = '{self.theme_dir}'")

    def install_theme(self) -> None:
        """Copying theme boilerplate"""
        theme_source_dir = pkg_resources.resource_filename(
            "homefront", _DEFAULT_THEME)

        shutil.copytree(theme_source_dir, self.theme_dir)

    def install_bootstrap(self) -> None:
        """Installing bootstrap"""
        version = self.settings["BOOTSTRAP_VERSION"]

        cachedir = homefront.settings.get_cache_dir(
            self.settings, self.base_dir)

        os.makedirs(cachedir, exist_ok=True)

        bootstrap_dir = os.path.join(cachedir, f"bootstrap-{version}")
        homefront.bootstrap.download(version, bootstrap_dir)

        os.makedirs(os.path.join(self.theme_dir, "scss"), exist_ok=True)

        for filename in ("_variables.scss", ):
            shutil.copy(
                os.path.join(bootstrap_dir, "scss", "bootstrap", filename),
                os.path.join(self.theme_dir, "scss", filename))

    def create_package_json(self) -> None:
        """Creatinge nodejs package.json file"""
        package_json_filename = os.path.join(
            self.theme_dir, "js", "package.json")

        with open(package_json_filename, "w") as package_json:
            site_name = self.settings['SITENAME']
            contents = {
                "name": site_name,
                "version": f"{datetime.date.today():%Y%m%d}.0.0",
                "description": f"Javascripts of {site_name}",
                "private": True,
                "dependencies": {
                    # "google-closure-compiler": "20190301.0.0",
                    "jquery": "^3.4.1",
                    "popper.js": "^1.15.0",
                    "bootstrap": "^" + self.settings['BOOTSTRAP_VERSION'],
                },
                "devDependencies": {},
                "author": self.settings["AUTHOR"],
                "license": "Rights reserved"
            }

            json.dump(contents, package_json, indent=2)

    def create_gitignore(self) -> None:
        with open(os.path.join(self.base_dir, ".gitignore"), "a") as gitignore:
            gitignore.write(
                "\n# Added by homefront\n"
                "__pycache__\n"
            )

            gitignore.write(
                os.path.join(self.theme_dir, 'js', "node_modules\n"))

            for ignored in ("CACHE_PATH", "OUTPUT_PATH", ):
                ignored = (self.settings[ignored].rstrip(os.path.sep) +
                           os.path.sep)
                gitignore.write(f"{ignored}\n")


def main():
    base_dir = pelican_quickstart()

    print("Creating Homefront project")
    website = Website(base_dir)

    step(website.update_settings)
    step(website.install_theme)
    step(website.install_bootstrap,
         details=website.settings["BOOTSTRAP_VERSION"])
    step(website.create_package_json)
    step(website.create_gitignore)

    print("Done, homefront project structure created")
    print(f"You can customize the theme in {website.theme_dir}")
