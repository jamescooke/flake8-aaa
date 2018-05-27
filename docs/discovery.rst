Test discovery
==============

* Filename must start with ``test_`` and have been collected for linting by
  ``flake8``.

* Test must be a function where its name starts with ``test``.

* Tests that contain only comments, docstrings or ``pass`` are skipped.
