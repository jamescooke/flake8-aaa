.. image:: https://img.shields.io/travis/jamescooke/flake8-aaa/master.svg
    :target: https://travis-ci.org/jamescooke/flake8-aaa/branches
    :alt: Travis build

.. image:: https://img.shields.io/readthedocs/flake8-aaa.svg
    :alt: Read the Docs
    :target: https://flake8-aaa.readthedocs.io/

.. image:: https://img.shields.io/pypi/v/flake8-aaa.svg
    :alt: PyPI
    :target: https://pypi.org/project/flake8-aaa/

.. image:: https://img.shields.io/pypi/pyversions/flake8-aaa.svg
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/flake8-aaa/

.. image:: https://img.shields.io/github/license/jamescooke/flake8-aaa.svg
    :alt: flake8-aaa is licensed under the MIT License
    :target: https://github.com/jamescooke/flake8-aaa/blob/master/LICENSE


Flake8-AAA
==========

A linter for Python tests.

* Pytest and unittest styles supported.

* Tests are linted against the `Arrange Act Assert pattern
  <http://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html>`_.

* Provides a Flake8 interface to automatically lint test files as part of your
  Flake8 run.

* Provides a command line interface for custom (non-Flake8) usage and
  debugging.

Installation
------------

Install with ``pip``::

    $ pip install flake8-aaa

Integration with Flake8
-----------------------

Given that you already have Flake8 installed in the same environment, check
that Flake8-AAA was installed correctly by asking ``flake8`` for its version
signature::

    $ flake8 --version
    3.6.0 (aaa: 0.4.0, mccabe: 0.6.1, pycodestyle: 2.4.0, pyflakes: 2.0.0) CPython 3.6.7 on Linux

The ``(aaa: 0.4.0, ...`` part of that output tells you ``flake8`` found this
plugin. Now you can run ``flake8`` as usual against your project and Flake8-AAA
will lint your tests via its plugin::

    $ flake8


Resources
---------

* `Documentation on ReadTheDocs <https://flake8-aaa.readthedocs.io/>`_

* `Package on PyPI <https://pypi.org/project/flake8-aaa/>`_

* `Source code on GitHub <https://github.com/jamescooke/flake8-aaa>`_

* `Licensed on MIT <https://github.com/jamescooke/flake8-aaa/blob/master/LICENSE>`_

* `Changelog <https://github.com/jamescooke/flake8-aaa/blob/master/CHANGELOG.rst>`_

Tested on Pythons 3.5 and 3.6.

Python 2 supported up to ``v0.4.0``:
`pypi <https://pypi.org/project/flake8-aaa/0.4.0/>`_,
`docs <https://flake8-aaa.readthedocs.io/en/v0.4.0/>`_,
`tag <https://github.com/jamescooke/flake8-aaa/releases/tag/v0.4.0>`_.
