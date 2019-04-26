# coding: utf-8
import pelican.generators

import homefront.settings


class Generator(pelican.generators.Generator):
    """
    Base class for all pelican generators in the package.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        homefront.settings.update(self.settings)
