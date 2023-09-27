Requirements management
=======================

TL;DR
-----

To update all requirements:

.. code-block:: shell

    rm requirements/*.txt
    tox -m requirements

Summary
-------

* ``ci.in|txt``: Packages for GitHub Actions built with Python 3.10.

* ``dev.in|txt``: Packages for working on code. Build with Python 3.8.

* ``test.in|txt``: Test packages for Tox environments. Build with Python 3.8.

* ``examples.in|txt``: Test packages for Tox, also Python 3.8.

* ``docs.in|txt``: Python 3.10 (match RTD)

CI requirements
---------------

``ci.txt``: Python 3.10

Used by GitHub Actions. Installs tox and GH helper to manage Python versions.

Targets Python 3.10 because GHA instance uses that version in ``ubuntu-22.04``
image.

Tox dependency is pinned to allow for tags to be built "in the past". For
example, in scenarios where they might have missed a build / were forgotten.
E.g. `tag v0.12.2
<https://github.com/jamescooke/flake8-aaa/releases/tag/v0.12.2>`_ was added
more than a year after the release was done, but by that point couldn't be
built by latest Tox, so `commit 77e29
<https://github.com/jamescooke/flake8-aaa/commit/77e29b1bbfaebed1664bcbc4bb77580185f00ae8>`_
now shows red 😞.

Development requirements
------------------------

``dev.txt``: Python 3.8

Targets Python 3.8 because it's the oldest supported Python version.

All tools for local development. Tests are run in Tox, so no Pytest. But
linters are run in editor, so those are installed.

Twine available for shipping packages.
