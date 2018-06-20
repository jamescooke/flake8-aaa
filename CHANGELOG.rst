Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog
<http://keepachangelog.com/en/1.0.0/>`_ and this project adheres to `Semantic
Versioning <http://semver.org/spec/v2.0.0.html>`_.


Unreleased_
-----------

Added
-----

* New rule ``AAA03`` "expected 1 blank line before Act block, found none"

0.2.0_ - 2018/05/28
-------------------

Added
.....

* `Documentation on RTD <https://flake8-aaa.readthedocs.io/>`_

Fixed
.....

* Allow parsing of files containing unicode.

* Do not parse ``pytest.raises`` blocks in Assert block as Actions.

0.1.0 - 2018/04/13
------------------

Initial alpha release.

.. _Unreleased: https://github.com/jamescooke/flake8-aaa/compare/v0.2.0...HEAD
.. _0.2.0: https://github.com/jamescooke/flake8-aaa/compare/v0.1.0...v0.2.0
