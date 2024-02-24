Release checklist
=================

The following tasks need to be completed for each release of Flake8-AAA. They
are mainly for the maintainer's use.

Bumping packages
----------------

This is handled by ``tox`` which calls the ``requirements/Makefile``. Trigger a
full rebuild of requirements by deleting all compiled ``.txt`` files and asking
for a compilation:

.. code-block:: shell

    rm requirements/*.txt
    tox r -m requirements

Versioning
----------

Given a new version called ``x.y.z``:

* Create a branch for the new release. Usually called something like
  ``bump-x.y.z``.

* Run ``./bump_version.sh [x.y.z]``.

* Ensure command line output examples in ``README.rst`` are up to date. Run:

  .. code-block:: shell

      make signature

  Update the version string in the README and compatibility doc.

* Commit changes and push ``bump-x.y.z`` branch for testing. Use ``Bump to
  x.y.z`` as the PR title.

Merge
-----

* When branch ``bump-x.y.z`` is green, then merge it to ``master``. All pull
  requests are "squash merged".

* Update master locally and ensure that you remain on master for the rest of
  the process.

Test PyPI
---------

* Test that a build can be shipped to test PyPI with ``make testpypi``.

* After successful push, check the `TestPyPI page
  <https://test.pypi.org/project/flake8-aaa/>`_.  

Tag and push
------------

* Tag the repo with ``make tag``. Add a short message describing the key
  feature of this release.

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
