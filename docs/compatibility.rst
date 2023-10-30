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

Requires Flake8 version 3 and later. All integration tests run with the latest
version of Flake8 for the active version of Python.

We use the newer plugin system implemented in Flake8 v3.

Check that Flake8-AAA was installed correctly by asking ``flake8`` for its
version signature:

.. code-block:: shell

    flake8 --version

.. code-block::

    6.1.0 (flake8-aaa: 0.17.0, mccabe: 0.7.0, pycodestyle: 2.11.1, pyflakes: 3.1.0) CPython 3.11.6 on Linux

The ``flake8-aaa: 0.17.0`` part of that output tells you Flake8 found this
plugin.

Yapf
----

`Yapf <https://github.com/google/yapf>`_ is used to format Flake8-AAA code and
tests. It is the primary formatter focused on for compatibility.

Black
-----

Flake8-AAA is compatible with tests formatted with `Black
<https://github.com/psf/black>`_.

Black version ``23.1.0`` changed how it managed blank lines by default. Set
:ref:`"large" Act block style option or configuration <large-act-block-style>`
when running via Flake8 for best compatibility with Black:

.. code-block:: shell

    flake8 --aaa-act-block-style=large

See also `Black formatted example tests
<https://github.com/jamescooke/flake8-aaa/tree/master/examples/#black-formatted-examples>`_
in Flake8-AAA's test suite.

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

Python 3.7
..........

Python 3.7 was supported up to ``v0.15.0``

* `v0.15.0 on PyPI <https://pypi.org/project/flake8-aaa/0.15.0/>`_
* `v0.15.0 Documentation <https://flake8-aaa.readthedocs.io/en/v0.15.0/>`_
* `Github v0.15.0 tag
  <https://github.com/jamescooke/flake8-aaa/releases/tag/v0.15.0>`_

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
