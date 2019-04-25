# coding: utf-8
"""
Wraps and extends the pelican-quickstart tool to create directories for Sass
(CSS) and Javascript sources.
"""

import pelican.tools.pelican_quickstart


def main():
    pelican.tools.pelican_quickstart.main()

    # PELICAN_CONF = pelican.tools.pelican_quickstart.CONF

    # TODO add homefront plugins
    # TODO create sass and js directory
    # TODO checkout bootstrap (download the tarball)

    # TODO add gitignore with: cache, output, __pycache__
