Flake8-AAA
==========

.. image:: https://img.shields.io/travis/com/jamescooke/flake8-aaa/master.svg
    :target: https://travis-ci.com/jamescooke/flake8-aaa/branches
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

..

A Flake8 plugin that checks Python tests follow the Arrange-Act-Assert pattern.

----------

📝 Table of Contents
-------------------

* About

🧐 About
-------

What is the Arrange-Act-Assert pattern?
.......................................

The "Arrange-Act-Assert" pattern (also known as "AAA" and "3A") was observed
and named by Bill Wake in 2001. The pattern focuses each test on a single
object's behaviour.

As the name suggests each test is broken down into three distinct parts:

* **Arrange:** Set up the object to be tested.

* **Act**: Carry out an action on the object.

* **Assert**: Check the object changed as expected, make claims about results
  and collaborating objects.

This all sounds very abstract, so here's a simple example. It is a simple test
on the behaviour of add ``+`` on two integers:

.. code-block:: python

   def test():
      x = 1
      y = 1

      result = x + y

      assert result == 2

As you can see, the Act block starts with ``result =`` and is separated from
the Arrange and Assert blocks by blank lines. The test is focused - it only
contains one add operation and no further additions occur.

Using AAA consistently makes it easier to find the Action in a test. It's
therefore always easy to see the object behaviour each test is focused on.

Further reading:

* `Arrange Act Assert pattern for Python developers
  <https://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html>`_
  - includes more information about the pattern and each part of a test.

* `Our "good" example files
  <https://github.com/jamescooke/flake8-aaa/tree/master/examples/good>`_ -
  these contain more test examples which we use in our test suite.

What is Flake8?
...............

Flake8 is a command line utility for enforcing style consistency across Python
projects. It wraps multiple style checking tools and also runs third-party
checks provided by plugins, of which Flake8-AAA is one.

Further reading:

* `Flake8's documentation <https://flake8.pycqa.org/en/latest/>`_ 

* `Awesome Flake8 Extensions
  <https://github.com/DmytroLitvinov/awesome-flake8-extensions/>`_ - a list of
  Flake8 plugins.

What does Flake8-AAA do?
........................

Flake8-AAA extends Flake8 to check your Python tests match the AAA pattern.

It does this by adding the following new checks to Flake8:

* Every test has a single clear Act block.

* Every Act block is distinguished from the code around it with a blank line
  above and below.

* Arrange and Assert blocks do not contain additional blank lines.

Checking your code with these simple formatting rules helps you write simple,
consistently formatted tests that match the AAA pattern. They are most helpful
if you call Flake8 regularly, for example when you save a file or before you
run a test suite.

In the future, Flake8-AAA will check that no test has become too complicated.

Installation and usage
----------------------

Flake8-AAA is a Flake8 plugin.

Install ``flake8-aaa`` with ``pip``, which will also install ``flake8``::

    $ pip install flake8-aaa

Invoke Flake8 on your test suite, in this case in the ``tests`` directory::

    $ flake8 tests

Errors returned by Flake8-AAA have the AAA code, for example::

    tests/block/test_init.py:14:1: AAA02 multiple Act blocks found in test


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
