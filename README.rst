.. image:: https://img.shields.io/travis/jamescooke/flake8-aaa/master.svg
    :target: https://travis-ci.org/jamescooke/flake8-aaa/branches
    :alt: Travis build

.. image:: https://img.shields.io/readthedocs/flake8-aaa.svg
    :alt: Read the Docs
    :target: https://flake8-aaa.readthedocs.io/

.. image:: https://img.shields.io/pypi/v/flake8-aaa.svg
    :alt: PyPI
    :target: https://pypi.org/project/flake8-aaa/

.. image:: https://img.shields.io/pypi/pyversions/flake8-aaa.svg
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/flake8-aaa/

.. image:: https://img.shields.io/github/license/jamescooke/flake8-aaa.svg
    :alt: flake8-aaa is licensed under the MIT License
    :target: https://github.com/jamescooke/flake8-aaa/blob/master/LICENSE


Flake8-AAA
==========

    A linter for Python tests.

Flake8-AAA enforces simple formatting of your test suite making it more
consistent and easier to grok, especially across teams.

Installation and usage
----------------------

Flake8-AAA is a Flake8 plugin.

Install ``flake8-aaa`` with ``pip``, which will also install ``flake8``::

    $ pip install flake8-aaa

Invoke Flake8 on your test suite, in this case in the ``tests`` directory::

    $ flake8 tests

Errors returned by Flake8-AAA have the AAA code, for example::

    tests/block/test_init.py:14:1: AAA02 multiple Act blocks found in test

Arrange Act Assert
------------------

Tests are linted against the `Arrange Act Assert pattern
<http://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html>`_.

TL;DR following the AAA pattern means tests are laid out like this:

.. code-block:: python

    def test():
        """
        __docstring__
        """
        <ARRANGE block> # set up of the system under test (SUT)
 
        <ACT block> # perform a single action on the SUT
 
        <ASSERT block> # check that the SUT changed as expected

For example:

.. code-block:: python

    def test(tmpdir):
        """
        Checker is able to parse provided file at load time
        """
        target_file = tmpdir.join('test.py')
        target_file.write('assert 1 + 2 == 3\n')
        tree = ast.parse(target_file.read())
        checker = Checker(tree, ['assert 1 + 2 == 3\n'], target_file.strpath)

        result = checker.load()

        assert result is None
        assert len(checker.tree.body) == 1
        assert type(checker.tree.body[0]) == ast.Assert
        assert len(checker.ast_tokens.tokens) == 8

More examples are in our `test suite's "good" files
<https://github.com/jamescooke/flake8-aaa/tree/master/examples/good>`_.


Compatibility
-------------

* Pytest and unittest supported.

* Compatible with Black and yapf formatted code.

* Compatible with type-annotated code, checked with mypy.

* Current release works with the latest versions of Python 3 (3.6, 3.7 and
  3.8). Older releases have support for older Pythons.

See the `Compatibility list
<https://flake8-aaa.readthedocs.io/en/stable/compatibility.html>`_ for more
info.


Resources
---------

* `Documentation on ReadTheDocs <https://flake8-aaa.readthedocs.io/>`_

* `Package on PyPI <https://pypi.org/project/flake8-aaa/>`_

* `Source code on GitHub <https://github.com/jamescooke/flake8-aaa>`_

* `Licensed on MIT <https://github.com/jamescooke/flake8-aaa/blob/master/LICENSE>`_

* `Changelog <https://github.com/jamescooke/flake8-aaa/blob/master/CHANGELOG.rst>`_
