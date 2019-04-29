Homefront
=========

Homefront is a boilerplate for a static website in Python, it provides a
skeleton to build a static website, supports SASS files compiled to CSS,
minified js, etc.

It is based on:

* `Pelican <https://blog.getpelican.com/>`_,
* `Bootstrap <https://getbootstrap.com/>`_ (and
  `Sass <https://sass-lang.com/>`_),
* `Google closure compiler <https://developers.google.com/closure/compiler/>`_.

Project status
--------------

Please be advised that I don't intend to provide any kind of support nor
actively maintain this project.

While I'm open to pull requests, do not expect me to work on bugs or implement
features requested in issues if I don't need them.

In order to avoid external dependencies (java, node, npm), Homefront uses the
native distribution of the Google closure compiler.

It is possible to add support for other platforms with java in roughly the same
fashion (see ``homefront/googleclosure.py``).

License
-------

The content of this repository is under Apache 2 license, with the possible
exception of embedded vendors, which are bundled with there respective LICENSE
file.

Quickstart
----------

Install it with::

   python setup.py

Run ``homefront-quickstart`` instead of ``pelican-quickstart``.

This will create a skeleton in the destination folder of your choice. It
contains a ``themes/default/scss/`` directory with:

* ``main.scss``: root style file, includes all dependencies, this is where you
  should enable or not the modules of bootstrap that you want.
* ``_variables.scss``: a copy of bootstrap's variables files, that can be
  customized,
* ``_theme.scss``: your own styles.

See ``homefront/settings.py`` to see which settings can be configured.

Use ``pelican`` to generate the website.

If you don't want to use ``homefront-quickstart``, you can simply install it
and enable these plugins in your existing pelican configuration:

* ``homefront.bootstrap``: installs and adds bootstrap as a dependency to your
  SCSS files, bootstrap files are included prefixed with ``bootstrap/`` (ex:
  ``@import "bootstrap/transitions";``,
* ``homefront.sass``: implicitly loaded by the bootstrap plugin, can be used
  if you want to compile scss files without using bootstrap.
* ``homefront.googleclosure``: used to minify JS files.
