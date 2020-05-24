Compatibility list
==================

Flake8-AAA is compatible with the following software. Future versions will
maintain this compatibility as closely as possible.

Python
------

Works with Python 3.

Flake8-AAA is fully compatible and tested against the latest versions of Python
3. Currently that's 3.6, 3.7 and 3.8.

The following versions of Python are no longer supported:

Python 3.5
..........

Python 3.5 was supported up to ``v0.7.2``

  * `v0.7.2 on PyPI <https://pypi.org/project/flake8-aaa/0.7.2/>`_
  * `v0.7.2 Documentation <https://flake8-aaa.readthedocs.io/en/v0.7.2/>`_
  * `Github v0.7.2 tag
    <https://github.com/jamescooke/flake8-aaa/releases/tag/v0.7.2>`_

Python 2
........

Python 2 was supported up to ``v0.4.0``

  * `v0.4.0 on PyPI <https://pypi.org/project/flake8-aaa/0.4.0/>`_
  * `v0.4.0 Documentation <https://flake8-aaa.readthedocs.io/en/v0.4.0/>`_
  * `Github v0.4.0 tag
    <https://github.com/jamescooke/flake8-aaa/releases/tag/v0.4.0>`_

Flake8
------

Works with Flake8 version 3 and later.

We use the newer plugin system implemented in Flake8 v3. This dependency is not
specified in ``setup.py`` because users may only want to use the command line
interface.

Check that Flake8-AAA was installed correctly by asking ``flake8`` for its
version signature::

    $ flake8 --version
    3.8.2 (aaa: 0.10.0, mccabe: 0.6.1, pycodestyle: 2.6.0, pyflakes: 2.2.0) CPython 3.6.10 on Linux

The ``aaa: 0.10.0`` part of that output tells you Flake8 found this plugin.

Yapf
----

Yapf is used to format Flake8-AAA code and tests. It is the primary formatter
focused on for compatibility.

Black
-----

Flake8-AAA is compatible with tests formatted with Black.

    The coding style used by Black can be viewed as a strict subset of PEP8.

The AAA pattern is PEP8 compatible so it makes sense that Flake8-AAA should
work with PEP8 compatible formatters.

This compatibility is pinned by the test examples in the `examples/good/black
directory
<https://github.com/jamescooke/flake8-aaa/tree/master/examples/good/black>`_.
These tests are formatted with the latest version of Black in default mode.
They are then checked to pass Flake8-AAA's linting.

Pytest
------

Pytest is fully supported.

To pin this compatibility we use the latest version of Pytest in the
Flake8-AAA test suite and lint that test suite with Flake8-AAA (aka. dog
fooding).

Unittest
--------

Python unittest style is supported.

To pin this compatibility we include unittest-style tests in the `examples/good
directory
<https://github.com/jamescooke/flake8-aaa/tree/master/examples/good>`_ -
