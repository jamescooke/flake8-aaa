Requirements management
=======================

Summary
-------

* CI: Python 3.10

* dev: Python 3.8 (can't build on 3.7)

* Tox envs:

  * test: Python 3.7 - used by ``lint`` and ``test`` environments.

  * docs: Python 3.10 (match RTD)

CI ``ci.txt`` py310
-------------------

Used by GitHub Actions. Installs tox and GH helper to manage Python versions.

# Requirements for CI
# Currently GitHub actions on their Ubuntu 22.04 images
# These have Python 3.10.6 installed so compile these requirements with py310
# https://github.com/actions/runner-images/blob/main/images/linux/Ubuntu2204-Readme.md

Targets Python 3.10 because GHA instance uses that version in ``ubuntu-22.04``
image.

Am using a pinned Tox dependency to allow for tags to be built "in the past" in
scenarios where they might have missed a build / were forgotten. E.g. `tag
v0.12.2 <https://github.com/jamescooke/flake8-aaa/releases/tag/v0.12.2>`_ was
added more than a year after the release was done, but by that point couldn't
be built by latest Tox, so `commit 77e29
<https://github.com/jamescooke/flake8-aaa/commit/77e29b1bbfaebed1664bcbc4bb77580185f00ae8>`_
now shows red 😞.

Development ``dev.txt`` py38
----------------------------

Targets Python 3.8 because it's the oldest version that is easy to build these
requirements for (Python 3.7 fails to build this list with no constraints).

All tools for local development. Tests are run in Tox, so no Pytest. But
linters are run in editor, so those are installed.

Twine available for shipping packages
