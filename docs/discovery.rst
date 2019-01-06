Test discovery
==============

The ``flake8-aaa`` plugin is triggered for files that look to it like test
modules - anything that does not look like a test module is skipped.

The following rules are applied by ``flake8-aaa`` when discovering tests:

* The module's filename must start with "test\_" and have been collected for
  linting by Flake8.

* Every function in the module that has a name that starts with "test" is
  checked.

* Test functions can be class methods.

* Test functions that contain only comments, docstrings or ``pass`` are
  skipped.

These rules are aimed to mirror pytest's default collection strategy as closely
as possible.

If you find that ``flake8-aaa`` is giving false positives (you have checks that
you expected to fail, but they did not), then you should check that the plugin
did not ignore or skip those tests which you expected to fail.

.. note::

    ``flake8-aaa`` does not check doctests.


Processing
----------

For each test found, Flake8-aaa runs the following process:

Check for no-op
...............

Skip test if it is considered "no-op" (``pass``, docstring, etc).

Process Act Block
.................

Search the test for an "Action Node" which will indicate the existence of an
Act Block. There are four recognised types of Action Node:

``marked_act``
    Action is marked with Marked with ``# act`` comment::

        do_thing()  # act

``pytest_raises``
    Action is wrapped in ``pytest.raises`` context manager::

        with pytest.raises(ValueError):
            do_thing()

``result_assignment``
    Simple ``result =`` action::

        result = do_thing()

``unittest_raises``
    Action is wrapped in unittest's ``assertRaises`` context manager::

        with self.assertRaises(ValueError):
            do_thing()

If no Action Node is found then TODO link: "AAA01: no Act block found in test"
is raised.

Next the footprint of the Action Node is generated to create the Act Block.
Most Act Block footprints will be the same as the Action Node's footprint, for
example::

    ACT     with pytest.raises(ValueError):   # <- Action Node
    ACT         do_thing()                    # <- Action Node

However, Action Nodes can be wrapped in loops and context managers which must
be checked and incorporated when appropriate, for example::

    ACT     with mock.patch(thing_doer) as mock_thing_doer:
    ACT         result = do_thing()           # <- Action Node
