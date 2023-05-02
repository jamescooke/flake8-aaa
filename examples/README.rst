Examples
========

Test examples used to test Flake8-AAA.

Layout
------

* ``bad``: Examples that fail linting. Executed with default config.

* ``black``: Examples formatted with Black. As of version ``23.1.0``, these
  require ``--aaa-act-block-style=large`` to pass.

* ``data``

* ``good``: Test examples that all pass linting with default config. These are
  run with no options or config; default options; and default config.

* ``good_py38``

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
