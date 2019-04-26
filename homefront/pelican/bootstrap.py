# coding: utf-8
from typing import Type

import logging

import pelican
import pelican.signals

import homefront.generators

LOG = logging.getLogger(__name__)


class SaasGenerator(homefront.generators.Generator):
    """
    Compile and minify sass files and move them to a static folder.
    """
    def generate_context(self) -> None:
        pass

    def generate_output(self, writer) -> None:
        pass


class BootstrapGenerator(SaasGenerator):
    def ensure_bootstrap_in_cache(self):
        raise NotImplementedError(self.settings["BOOTSTRAP_VERSION"])

    def remove_bootstrap(self):
        # remove from cache, let's use a cache/homefront/bootstrap_version to
        # store the version, and re-install if not compat
        pass

    def generate_output(self, writer):
        self.ensure_bootstrap_in_cache()
        super().generate_output(writer)


def get_generators(_: pelican.Pelican) -> Type[BootstrapGenerator]:
    """
    Return the class of the generator implemented by this plugin.
    """
    return BootstrapGenerator


def register():
    """
    Register pelican signal handlers.
    """
    pelican.signals.get_generators.connect(get_generators)


"""
TODO:
* implement a new generator which generate sass files
usually we've got a pelican object as a parameter of the generator
check its content, there's probably the settings

* maybe a homefront.settings.get(pelican, settingname) -> setting with possible
override or default from homefront

* add a bootstrap.lock in homefront cache with version

* above functions better be in a class with the pelican object, no?



====
* how to log stuff with pelican in a plugin? >>>> logging cool
"""
