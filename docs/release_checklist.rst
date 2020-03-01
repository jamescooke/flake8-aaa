Release checklist
=================

Items to be completed before and after each release.

Pre-release steps
-----------------

Given a new version called ``x.y.z``:

* Create a branch for the new release. Usually called something like
  ``bump-vx.y.z``.

* Run ``./bump_version.sh [x.y.z]``.

* Commit changes and push ``bump-vx.y.z`` branch for testing.

* Now is a good time to build and check the documentation locally.

  - Ensure that command line output examples are up to date. They can be
    updated using the output of the ``cmd`` and ``cmdbad`` ``tox``
    environments.

* When branch ``bump-vx.y.z`` is green, then merge it to ``master``.

* Update master locally and ensure that you remain on master for the rest of
  the process.

* Test that a build can be shipped to test PyPI with ``make testpypi``. (Every
  build runs the full clean test suite locally to ensure that nothing has
  broken before building)

* After successful push, check the `TestPyPI page
  <https://test.pypi.org/project/flake8-aaa/>`_.

* Then tag the repo with ``make tag``. Add a short message about what the key
  change is.

* Make the new tag public with ``git push origin --tags``.

* Build and push to PyPI with ``make pypi``.

* After successful push, check the `PyPI page
  <https://pypi.org/project/flake8-aaa/>`_.

Post release checks
-------------------

* Visit the `CHANGELOG
  <https://github.com/jamescooke/flake8-aaa/blob/master/CHANGELOG.rst>`_
  and ensure that the new release's comparison link works with the new tag.

* Check the `RTD builds
  <https://readthedocs.org/projects/flake8-aaa/builds/>`_ to ensure that the
  latest documentation version has been picked up and that the ``stable`` docs
  are pointed at it.

  A new docs release will not have been created for the new tag as per `this
  issue <https://github.com/rtfd/readthedocs.org/issues/3508>`_. Click "Build
  Version:" on the builds page for the new tag to be picked up.
