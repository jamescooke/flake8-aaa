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


flake8-aaa
==========

A `flake8 <http://flake8.pycqa.org/en/latest/index.html>`_ plugin for linting
Python tests against the rules of the `Arrange Act Assert pattern
<http://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html>`_
of testing.


Installation
------------

Install with ``pip``::

    $ pip install flake8-aaa

Check that ``flake8-aaa`` was installed correctly by asking ``flake8`` for its
version signature::

    $ flake8 --version
    3.5.0 (aaa: 0.3.0, mccabe: 0.6.1, pycodestyle: 2.3.1, pyflakes: 1.6.0) CPython 3.5.2 on Linux

The ``aaa: 0.3.0`` part of that output tells you ``flake8`` found this plugin.

There is more information on invoking ``flake8`` on the `Invoking Flake8
<http://flake8.pycqa.org/en/latest/user/invocation.html>`_ documentation page.

See the `full list of error codes on ReadTheDocs
<https://flake8-aaa.readthedocs.io/en/stable/rules.html>`_.


Resources
---------

* `Documentation on ReadTheDocs <https://flake8-aaa.readthedocs.io/>`_

* `Package on PyPI <https://pypi.org/project/flake8-aaa/>`_

* `Source code on GitHub <https://github.com/jamescooke/flake8-aaa>`_

* `Licensed on MIT <https://github.com/jamescooke/flake8-aaa/blob/master/LICENSE>`_

* `Changelog <https://github.com/jamescooke/flake8-aaa/blob/master/CHANGELOG.rst>`_

Tested on Pythons 2.7 and 3.6.
