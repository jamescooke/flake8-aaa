Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog
<http://keepachangelog.com/en/1.0.0/>`_ and this project adheres to `Semantic
Versioning <http://semver.org/spec/v2.0.0.html>`_.


Unreleased_
-----------

See also `latest documentation
<https://flake8-aaa.readthedocs.io/en/latest/>`_.

Changed
.......

* Install requires ASTTokens version 2 or greater, was previously
  ``>= 1.1.10``.

* Special test examples that only ran on Python 3.6 and greater, now merged
  into main test suite. `#128
  <https://github.com/jamescooke/flake8-aaa/pull/128>`_

Removed
.......

* Support for Python 3.5. `#110
  <https://github.com/jamescooke/flake8-aaa/issues/110>`_

* Pylint removed from linting checks.

0.7.2_ - 2020/02/24
-------------------

Fixed
.....

* Bug preventing type annotated assignment Act blocks from being found `#123
  <https://github.com/jamescooke/flake8-aaa/pull/123>`_

0.7.1_ - 2019/11/16
-------------------

Added
.....

* Expanded test suite to run Python 3.8 and added Python 3.8 meta tags. `#119
  <https://github.com/jamescooke/flake8-aaa/pull/119>`_

Fixed
.....

* Bug occurring when running Python 3.8 and linting test functions that are
  decorated has been fixed. `#119
  <https://github.com/jamescooke/flake8-aaa/pull/119>`_

0.7.0_ - 2019/07/14
-------------------

Added
.....

* Improved documentation on use of ``# noqa`` comments. `#102
  <https://github.com/jamescooke/flake8-aaa/issues/102>`_.

Changed
.......

* AAA03 and AAA04 (checks for a single blank line before and after Act block)
  line numbers have been moved down. `Part of #79
  <https://github.com/jamescooke/flake8-aaa/issues/79#issuecomment-495814091>`_.

* AAA03 and AAA04 errors now return a real offset. `#79
  <https://github.com/jamescooke/flake8-aaa/issues/79>`_.

0.6.2_ - 2019/06/29
-------------------

Added
.....

* Add tests for compatibility with Black to the test suite. `#90
  <https://github.com/jamescooke/flake8-aaa/issues/90>`_

* New compatibility list shows what Flake8-AAA works with now and plans to
  support in the future. `#97
  <https://github.com/jamescooke/flake8-aaa/issues/97>`_

Fixed
.....

* F-string processing was crashing Flake8-AAA with all versions of Python. This
  has been fixed with a workaround. `#101
  <https://github.com/jamescooke/flake8-aaa/issues/101>`_

  This will be "fully fixed" in the first minor version after support for
  Python 3.5 is dropped. `#110
  <https://github.com/jamescooke/flake8-aaa/issues/110>`_

0.6.1_ - 2019/05/26
-------------------

Added
.....

* Output the total number of errors found in a file from the command line
  interface, along with a big "PASSED!" or "FAILED"

* New test run ``cmdbad`` asserts that all bad example files return at least
  one error and a non-zero error code when run through the command line.

Fixed
.....

* Command line was not returning total number of errors in the file. Instead it
  was returning the number of errors in the last function. This meant that
  false positives were given for files that contained errors, but where the
  last test in the file contained none - in this case a ``0`` return value was
  given. `#90 <https://github.com/jamescooke/flake8-aaa/issues/90>`_


0.6.0_ - 2019/04/28
-------------------

Added
.....

* New rule ``AAA05`` "blank line in block". `#66
  <https://github.com/jamescooke/flake8-aaa/issues/66>`_.

Changed
.......

* Adjusted error handling so that multiple errors can be returned. `#76
  <https://github.com/jamescooke/flake8-aaa/issues/76>`_.

* Blank line analysis changed drastically. Now runs first as part of the test
  function analysis and finds all blank lines that are not part of a string
  literal.

0.5.2_ - 2019/02/27
-------------------

Added
.....

* Support for Python 3.7.

Changed
.......

* Act node now distinguished from Act block in code and docs. Generic ``Block``
  class now handles all blocks.

* Python warnings now reported in test runs.

* Command line wrapper fixed to manually close files opened by ``argparse``.

0.5.1_ - 2019/02/01
-------------------

Added
.....

* Bad examples folder. This is used for testing that files containing tests
  that fail linting return the expected content when run with ``flake8```.

Fixed
.....

* Spacing between Arrange and Act analysis fixed. Now recognises comment
  blocks.

* Spacing between Act and Assert analysis fixed. Now recognises comment blocks.

* Act Blocks can now contain context managers that are not test suite exception
  catchers like ``pytest.raises()``.

Changed
.......

* Location of package pushed down to ``/src`` directory as `recommended by
  pytest
  <https://docs.pytest.org/en/latest/goodpractices.html#choosing-a-test-layout-import-rules>`_.

0.5.0_ - 2018/11/01
-------------------

Added
.....

* Python 3.5 now supported.

* Command line functionality now available to assist with development and
  debugging.

* New line-wise analysis, including updated blank line checking and a new
  ``AAA99`` rule for node to line mapping collisions.

Removed
.......

* Python 2.7 support removed.

* ``flake8`` package removed as a dependency since Flake8-AAA can be run on a
  command line without it.

0.4.0_ - 2018/07/17
-------------------

Added
.....

* Support for unittest tests.

Changed
.......

* Improved loading of Act blocks so that they can be found within context
  managers.

0.3.0_ - 2018/06/28
-------------------

Added
.....

* New rule ``AAA03`` "expected 1 blank line before Act block, found none"

* New rule ``AAA04`` "expected 1 blank line before Assert block, found none"

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

.. _Unreleased: https://github.com/jamescooke/flake8-aaa/compare/v0.7.2...HEAD
.. _0.7.2: https://github.com/jamescooke/flake8-aaa/compare/v0.7.1...v0.7.2
.. _0.7.1: https://github.com/jamescooke/flake8-aaa/compare/v0.7.0...v0.7.1
.. _0.7.0: https://github.com/jamescooke/flake8-aaa/compare/v0.6.2...v0.7.0
.. _0.6.2: https://github.com/jamescooke/flake8-aaa/compare/v0.6.1...v0.6.2
.. _0.6.1: https://github.com/jamescooke/flake8-aaa/compare/v0.6.0...v0.6.1
.. _0.6.0: https://github.com/jamescooke/flake8-aaa/compare/v0.5.2...v0.6.0
.. _0.5.2: https://github.com/jamescooke/flake8-aaa/compare/v0.5.1...v0.5.2
.. _0.5.1: https://github.com/jamescooke/flake8-aaa/compare/v0.5.0...v0.5.1
.. _0.5.0: https://github.com/jamescooke/flake8-aaa/compare/v0.4.0...v0.5.0
.. _0.4.0: https://github.com/jamescooke/flake8-aaa/compare/v0.3.0...v0.4.0
.. _0.3.0: https://github.com/jamescooke/flake8-aaa/compare/v0.2.0...v0.3.0
.. _0.2.0: https://github.com/jamescooke/flake8-aaa/compare/v0.1.0...v0.2.0
