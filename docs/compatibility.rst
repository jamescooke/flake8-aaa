Compatibility list
==================

Flake8-AAA is compatible with the following software. Future versions will
maintain this compatibility as closely as possible.

Python
------

Works with Python 3.

Flake8-AAA is fully compatible and tested against the active versions of Python
3 as listed on the `python.org downloads page
<https://www.python.org/downloads/>`_.

.. admonition:: See also...

    See :ref:`full list of previously supported Python versions
    <previous-python-versions>` for links to the last supported packages and
    documentation.

Flake8
------

Works with Flake8 version 3 and later. All integration tests run with the
latest version of Flake8 they can find for the active version of Python.

We use the newer plugin system implemented in Flake8 v3. This dependency is not
specified in ``setup.py`` because users may only want to use the command line
interface.

Check that Flake8-AAA was installed correctly by asking ``flake8`` for its
version signature:

.. code-block:: shell

    flake8 --version

.. code-block::

    4.0.1 (aaa: 0.12.2, mccabe: 0.6.1, pycodestyle: 2.8.0, pyflakes: 2.4.0) CPython 3.10.1 on Linux

The ``aaa: 0.12.2`` part of that output tells you Flake8 found this plugin.

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

.. note::

    Black version ``23.1.0`` changed how it managed blank lines by default.
    This change causes Flake8-AAA to raise ``AAA03`` errors on tests that
    contain context managers and are formatted with Black. See `issue #200
    <https://github.com/jamescooke/flake8-aaa/issues/200>`_.

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
<https://github.com/jamescooke/flake8-aaa/tree/master/examples/good>`_.

.. _previous-python-versions:

Previous Python versions
------------------------

The following versions of Python are no longer supported:

Python 3.6
..........

Python 3.6 was supported up to ``v0.12.1``

* `v0.12.1 on PyPI <https://pypi.org/project/flake8-aaa/0.12.1/>`_
* `v0.12.1 Documentation <https://flake8-aaa.readthedocs.io/en/v0.12.1/>`_
* `Github v0.12.1 tag
  <https://github.com/jamescooke/flake8-aaa/releases/tag/v0.12.1>`_


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
