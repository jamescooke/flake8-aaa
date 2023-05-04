Examples
========

Test examples used to test Flake8-AAA.

Layout
------

* ``bad``: Examples that fail linting. Executed with default config.

* ``black``: Examples formatted with Black. As of version ``23.1.0``, these
  require ``--aaa-act-block-style=large`` to pass. See below for how to
  generate these files.

* ``data``

* ``good``: Test examples that all pass linting with default config. These are
  run with no options or config; default options; and default config.

* ``good_py38``

Black formatted examples
------------------------

To update the examples formatted with Black in ``examples/black`` (run from
project root)::

    make black_examples fixlintexamples

Then check them as part of the linting of example files::

    tox r -m lint_examples
