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

* `🧐 About`_
* `🏁 Getting Started`_
* `🎈 Usage`_

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

This all sounds very abstract, so here's a simple example that follows the
pattern - a simple test on the behaviour of add ``+``:

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
  - information about the pattern and each part of a test.

* `Our "good" example files
  <https://github.com/jamescooke/flake8-aaa/tree/master/examples/good>`_ -
  test examples used in the Flake8-AAA test suite.

What is Flake8?
...............

Flake8 is a command line utility for enforcing style consistency across Python
projects. It wraps multiple style checking tools and also runs third-party
checks provided by plugins, of which Flake8-AAA is one.

Further reading:

* `Flake8's documentation <https://flake8.pycqa.org/en/latest/>`_ 

* `Awesome Flake8 Extensions
  <https://github.com/DmytroLitvinov/awesome-flake8-extensions/>`_ - a curated
  list of Flake8 plugins.

What does Flake8-AAA do?
........................

Flake8-AAA extends Flake8 to check your Python tests match the AAA pattern.

It does this by adding the following checks to Flake8:

* Every test has a single clear Act block.

* Every Act block is distinguished from the code around it with a blank line
  above and below.

* Arrange and Assert blocks do not contain additional blank lines.

In the future, Flake8-AAA will check that no test has become too complicated.

Checking your code with these simple formatting rules helps you write simple,
consistently formatted tests that match the AAA pattern. They are most helpful
if you call Flake8 regularly, for example when you save a file or before you
run a test suite.

Flake8-AAA also provides a command line interface. Although this is primarily
for debugging, it can be used to check files if you don't want to install
Flake8.

Further reading:

* `Rules and error codes documentation
  <https://flake8-aaa.readthedocs.io/en/stable/rules.html>`_.

* `Command line documentation
  <https://flake8-aaa.readthedocs.io/en/stable/commands.html#command-line>`_.

🏁 Getting Started
-----------------

Prerequisites
.............

Install Flake8 with `pip <https://pip.pypa.io/en/stable/installing/>`_, if you
don't have it already:

.. code-block:: shell

    $ pip install flake8

Installation
............

Install ``flake8-aaa``:

.. code-block:: shell

    $ pip install flake8-aaa

You can confirm that Flake8 recognises the plugin by checking its version
string:

.. code-block:: shell

    $ flake8 --version
    3.7.9 (aaa: 0.9.0, mccabe: 0.6.1, pycodestyle: 2.5.0, pyflakes: 2.1.1) ...

The ``aaa: 0.9.0`` part tells you that Flake8-AAA was installed successfully
and its checks will be used by Flake8.

Further reading:

* `Flake8 installation instructions
  <https://flake8.pycqa.org/en/latest/index.html#installation-guide>`_.

First run
.........

TODO add good and bad example.

🎈 Usage
.......

Flake8-AAA is used in the same scenario as Flake8 - that usually means 

Invoke Flake8 on your test suite, in this case in the ``tests`` directory::

    $ flake8 tests

Errors returned by Flake8-AAA have the AAA code, for example::

    tests/block/test_init.py:14:1: AAA02 multiple Act blocks found in test

.. code-block:: shell

    $ flake8 --select AAA tests

Further reading:

* `Using Flake8 <https://flake8.pycqa.org/en/latest/user/index.html>`_.

Compatibility
-------------

Flake8-AAA works with:

* Pytest and unittest test suites.

* Black and yapf formatted code.

* Mypy and type-annotated code.

* Latest versions of Python 3 (3.6, 3.7 and 3.8).

Further reading:

* `Full compatibility list
  <https://flake8-aaa.readthedocs.io/en/stable/compatibility.html>`_ - includes
  information on support for older versions of Python.

Resources
---------

* `Documentation on ReadTheDocs <https://flake8-aaa.readthedocs.io/>`_

* `Package on PyPI <https://pypi.org/project/flake8-aaa/>`_

* `Source code on GitHub <https://github.com/jamescooke/flake8-aaa>`_

* `Licensed on MIT <https://github.com/jamescooke/flake8-aaa/blob/master/LICENSE>`_

* `Changelog <https://github.com/jamescooke/flake8-aaa/blob/master/CHANGELOG.rst>`_
