# coding: utf-8
from typing import Optional, Type, Union

import glob
import logging
import os

import pelican
import pelican.generators
import pelican.signals

import homefront
import homefront.release
import homefront.bootstrap
import homefront.pelican.sass

LOG = logging.getLogger(__name__)


class BootstrapPlugin:
    _instance = None

    @classmethod
    def get(cls):
        """
        Returns a singleton instance of :class:`BootstrapPlugin`.

        We use a singleton because Blinker uses weak references.
        """
        if not cls._instance:
            cls._instance = cls()

        return cls._instance

    def __init__(self):
        self.pelican: pelican.Pelican = None
        self.enabled: bool = False
        self.bootstrap_path: Optional[Union[str, os.PathLike]] = None

        self.enable()

    @property
    def bootstrap_scss_path(self):
        return os.path.join(self.bootstrap_path, "scss")

    def enable(self) -> None:
        pelican.signals.initialized.connect(self.initialize)
        pelican.signals.get_generators.connect(self.get_generator)

        self.update_scss_include_path()

        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

        self.update_scss_include_path(enable=False)

        pelican.signals.get_generators.disconnect(self.get_generator)
        pelican.signals.get_generators.disconnect(self.initialize)

    def update_scss_include_path(self, enable: bool = True) -> None:
        if not self.bootstrap_path:
            return

        if enable:
            include_path = homefront.pelican.sass.SassGenerator.include_path
            include_path.append(self.bootstrap_scss_path)
        else:
            include_path = homefront.pelican.sass.SassGenerator.include_path
            include_path.remove(self.bootstrap_scss_path)

    def initialize(self, pelican_object: pelican.Pelican) -> None:
        self.pelican = pelican_object

        try:
            settings = pelican_object.settings
            homefront.settings.update(settings)
            self.bootstrap_path = self.ensure_bootstrap_ready(
                settings["BOOTSTRAP_VERSION"])

            LOG.debug("Bootstrap found at %s", self.bootstrap_path)

            LOG.info("Enabling bootstrap %s", settings["BOOTSTRAP_VERSION"])
            self.update_scss_include_path()
        except (homefront.Error, OSError):
            LOG.exception("Failed to initialize bootstrap, plugin deactivated")
            self.disable()

    def get_generator(self, _: pelican.Pelican  # pylint: disable=R0201
                      ) -> Type[pelican.generators.Generator]:
        """
        Return the class of the generator implemented by this plugin.
        """
        return homefront.pelican.sass.SassGenerator

    def ensure_bootstrap_ready(self, version: str) -> None:
        if not self.pelican:
            raise homefront.Error("Plugin homefront.bootstrap did not receive "
                                  "the initialized signal from pelican")

        LOG.debug("Checking bootstrap %s", version)

        cache_dir = homefront.settings.get_cache_dir(self.pelican.settings)
        bootstrap_path = os.path.join(cache_dir, f"bootstrap-{version}")

        # Bootstrap looks installed
        if os.path.isdir(bootstrap_path):
            return bootstrap_path

        pattern = os.path.join(cache_dir, "bootstrap-*/")
        for candidate in glob.iglob(pattern):
            candidate_version = os.path.basename(candidate)
            candidate_version = candidate_version.split("-", 1)[1]

            if homefront.release.version_matches(
                    version, candidate_version):
                return candidate

        # Couldn't find suitable version of bootstrap, let's install it
        homefront.bootstrap.download(version, bootstrap_path)
        return bootstrap_path


def register() -> None:
    """
    Register this pelican plugin.
    """
    BootstrapPlugin.get()
