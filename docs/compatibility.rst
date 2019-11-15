Compatibility list
==================

The stable version of Flake8-AAA is compatible with the following software.

Future versions will maintain this compatibility, unless an item is deprecated.

Python
------

Works with Python 3.

We fully test against the latest four versions of Python 3 - currently that's
3.5, 3.6, 3.7 and 3.8.

Support for Python 3.5 is deprecated and will end in December 2019.

Python 2
........

Python 2 is supported up to ``v0.4.0``

  * `PyPI <https://pypi.org/project/flake8-aaa/0.4.0/>`_
  * `Documentation <https://flake8-aaa.readthedocs.io/en/v0.4.0/>`_
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
    3.7.8 (aaa: 0.7.0, mccabe: 0.6.1, pycodestyle: 2.5.0, pyflakes: 2.1.1) CPython 3.6.7 on Linux

The ``aaa: 0.7.0`` part of that output tells you Flake8 found this plugin.

Black
-----

Tests formatted with latest Black version will pass.

    The coding style used by Black can be viewed as a strict subset of PEP8.

Given that the AAA pattern is PEP8 compatible it makes sense that Flake8-AAA
must work with test code that is formatted with PEP8 compatible formatters.
Therefore we'll maintain Flake8-AAA to pass with AAA-style tests formatted with
Black.

This compatibility is pinned by the test examples in the `examples/good/black
directory
<https://github.com/jamescooke/flake8-aaa/tree/master/examples/good/black>`_ -
we assert that these tests pass the latest version of Black's formatting and
Flake8-AAA's linting.

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
