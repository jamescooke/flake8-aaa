Flake8-AAA
==========

.. image:: https://img.shields.io/github/actions/workflow/status/jamescooke/flake8-aaa/build.yml?branch=master
    :alt: GitHub Workflow Status
    :target: https://github.com/jamescooke/flake8-aaa/actions?query=branch%3Amaster

.. image:: https://img.shields.io/readthedocs/flake8-aaa.svg
    :alt: Read the Docs
    :target: https://flake8-aaa.readthedocs.io/

.. image:: https://img.shields.io/pypi/v/flake8-aaa.svg
    :alt: PyPI
    :target: https://pypi.org/project/flake8-aaa/

.. image:: https://img.shields.io/pypi/dm/flake8-aaa
    :alt: PyPI monthly downloads
    :target: https://pypistats.org/packages/flake8-aaa

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
--------------------

* `About <#-about>`_
* `Getting Started <#-getting-started>`_
* `Usage <#-usage>`_
* `Compatibility <#-compatibility>`_
* `Resources <#-resources>`_

🧐 About
--------

What is the Arrange-Act-Assert pattern?
.......................................

"Arrange-Act-Assert" is a testing pattern that focuses each test on a single
object's behaviour. It's also known as "AAA" and "3A".

As the name suggests each test is broken down into three distinct parts
separated by blank lines:

* **Arrange:** Set up the object to be tested.

* **Act**: Carry out an action on the object.

* **Assert**: Check the expected results have occurred.

For example, a simple test on the behaviour of add ``+``:

.. code-block:: python

    def test() -> None:
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

* `Arrange-Act-Assert: A Pattern for Writing Good Tests
  <https://automationpanda.com/2020/07/07/arrange-act-assert-a-pattern-for-writing-good-tests/>`_
  - a great introduction to AAA from a Python perspective.

* `Anatomy of a test
  <https://docs.pytest.org/en/latest/explanation/anatomy.html>`_ - a
  description of Arrange Act Assert in the Pytest documentation.

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

* `Flake8's documentation <https://flake8.pycqa.org/en/latest/>`_.

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

In the future, Flake8-AAA will check that no test has become too complicated
and that Arrange blocks do not contain assertions.

Checking your code with these simple formatting rules helps you write simple,
consistently formatted tests that match the AAA pattern. They are most helpful
if you call Flake8 regularly, for example when you save a file or before you
run a test suite.

Further reading:

* `Error codes documentation
  <https://flake8-aaa.readthedocs.io/en/stable/error_codes/all.html>`_: A list
  of error codes raised by Flake8-AAA when a test doesn't match the AAA
  pattern.

🏁 Getting Started
------------------

Installation
............

Install ``flake8-aaa``:

.. code-block:: shell

    pip install flake8-aaa

This will install Flake8-AAA and its dependencies, which include Flake8.

You can confirm that Flake8 recognises the plugin by checking its version
string:

.. code-block:: shell

    flake8 --version

.. code-block::

    6.1.0 (flake8-aaa: 0.17.0, mccabe: 0.7.0, pycodestyle: 2.11.1, pyflakes: 3.1.0) CPython 3.11.6 on Linux

The ``flake8-aaa: 0.17.0`` part tells you that Flake8-AAA was installed
successfully and its checks will be used by Flake8.

Further reading:

* `Flake8 installation instructions
  <https://flake8.pycqa.org/en/latest/index.html#installation-guide>`_.

First run
.........

Let's check the good example from above. We expect Flake8 to return no errors:

.. code-block:: shell

    curl https://raw.githubusercontent.com/jamescooke/flake8-aaa/master/examples/good/test_example.py > test_example.py
    flake8 test_example.py

Silence - just what we wanted.

Now let's see a failure from Flake8-AAA. We can use a bad example:

.. code-block:: shell

    curl https://raw.githubusercontent.com/jamescooke/flake8-aaa/master/examples/bad/test.py > test.py
    flake8 test.py

.. code-block::

    test.py:4:1: AAA01 no Act block found in test

🎈 Usage
--------

Since Flake8-AAA is a Flake8 plugin, the majority of its usage is
dependent on how you use Flake8. In general you can point it at your source
code and test suite:

.. code-block:: shell

    flake8 src tests

If you're not already using Flake8 then you might consider:

* Adding a hook to your code editor to run Flake8 when you save a file.

* Adding a pre-commit hook to your source code manager to run Flake8 before you
  commit.

* Running Flake8 before you execute your test suite - locally or in CI.

If you just want Flake8-AAA error messages you can filter errors returned by
Flake8 with ``--select``:

.. code-block:: shell

    flake8 --select AAA tests

Further reading:

* `Flake8-AAA options and configuration
  <https://flake8-aaa.readthedocs.io/en/stable/options.html>`_.

* `Using Flake8 <https://flake8.pycqa.org/en/stable/user/index.html>`_.

⛏️ Compatibility
----------------

Flake8-AAA works with:

* Pytest and unittest test suites.

* Black and yapf formatted code.

* Mypy and type-annotated code.

* Active versions of Python 3 as listed on the `python.org downloads page
  <https://www.python.org/downloads/>`_.

Further reading:

* `Full compatibility list
  <https://flake8-aaa.readthedocs.io/en/stable/compatibility.html>`_ - includes
  how to configure Flake8-AAA to work with Black and information on support for
  older versions of Python.

📕 Resources
------------

* `Documentation on ReadTheDocs <https://flake8-aaa.readthedocs.io/>`_

* `Package on PyPI <https://pypi.org/project/flake8-aaa/>`_

* `Source code on GitHub <https://github.com/jamescooke/flake8-aaa>`_

* `Licensed on MIT <https://github.com/jamescooke/flake8-aaa/blob/master/LICENSE>`_

* `Changelog <https://github.com/jamescooke/flake8-aaa/blob/master/CHANGELOG.rst>`_

* `#flake8_aaa hashtag on Mastodon <https://fosstodon.org/tags/flake8_aaa>`_
