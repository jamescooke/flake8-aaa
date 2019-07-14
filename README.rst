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

* A Flake8 interface to automatically lint test files as part of your Flake8
  run.

* A command line interface for custom (non-Flake8) usage and debugging.

* Tests are linted against the `Arrange Act Assert pattern
  <http://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html>`_.

  TL;DR following the AAA pattern means tests look like this::

      def test():
          """
          __docstring__
          """
          <ARRANGE block> # set up of the system under test (SUT)

          <ACT block> # perform a single action on the SUT

          <ASSERT block> # check that the SUT changed as expected


  You might want to take a look `at the examples
  <https://github.com/jamescooke/flake8-aaa/tree/master/examples/good>`_.


Compatibility
-------------

* Pytest and unittest styles of testing supported.

* Compatible with Black formatted code.

* Tested on latest three versions of Python: 3.5, 3.6 and 3.7.

* Python 2 supported up to ``v0.4.0``:
  `pypi <https://pypi.org/project/flake8-aaa/0.4.0/>`_, `docs
  <https://flake8-aaa.readthedocs.io/en/v0.4.0/>`_, `tag
  <https://github.com/jamescooke/flake8-aaa/releases/tag/v0.4.0>`_.

See the "Compatibility list" on `ReadTheDocs
<https://flake8-aaa.readthedocs.io/>`_ for full info.

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
    3.7.8 (aaa: 0.7.0, mccabe: 0.6.1, pycodestyle: 2.5.0, pyflakes: 2.1.1) CPython 3.6.7 on Linux

The ``aaa: 0.7.0`` part of that output tells you Flake8 found this plugin. Now
you can run ``flake8`` as usual against your project and Flake8-AAA will lint
your tests via its plugin::

    $ flake8


Resources
---------

* `Documentation on ReadTheDocs <https://flake8-aaa.readthedocs.io/>`_

* `Package on PyPI <https://pypi.org/project/flake8-aaa/>`_

* `Source code on GitHub <https://github.com/jamescooke/flake8-aaa>`_

* `Licensed on MIT <https://github.com/jamescooke/flake8-aaa/blob/master/LICENSE>`_

* `Changelog <https://github.com/jamescooke/flake8-aaa/blob/master/CHANGELOG.rst>`_
