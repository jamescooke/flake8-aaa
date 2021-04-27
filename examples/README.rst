Examples
========

Test examples used to test Flake8-AAA.

Black formatted examples
------------------------

To update the examples formatted with Black in ``good/black`` (run from project
root)::

    pip install -r requirements/examples.txt
    make black_examples fixlintexamples

Then check them with "local" lint::

    make lintexamples

Or run tox on the "example" environments::

    tox -l | ag example
