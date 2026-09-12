Directives
==========

Flake8-AAA can be controlled using some special directives in the form of
comments in your test code.

Explicitly marking blocks
-------------------------

One can set the act block explicitly using the ``# act`` comment. This is
necessary when there is no assignment possible.

See :ref:`AAA01: no Act block found in test - Correct code 2 <aaa01-correct-code-2>`.

.. _disabling-flake8-aaa-selectively:

Disabling Flake8-AAA selectively
--------------------------------

When invoked via Flake8, Flake8 will filter any errors raised when lines are
marked with the ``# noqa`` syntax. You can turn off all errors from Flake8-AAA
by marking a line with ``# noqa: AAA`` and other Flake8 errors will still be
returned.

If you just want to ignore a particular error, then you can use the more
specific code and indicate the exact error to be ignored. For example, to
ignore the check for a space before the Act block, we can mark the Act block
with ``# noqa: AAA03``:

.. code-block:: python

    def test():
        x = 1
        result = x + 1  # noqa: AAA03

        assert result == 2

If you're working with ``unittest.TestCase.subTest()`` (currently unsupported),
you can use ``noqa: AAA`` on the test method declaration line to ignore each
test that has subtests.

.. code-block:: python

    def test_even(self) -> None:  # noqa: AAA
        """
        Example from stdlib docs: Test that numbers between 0 and 5 are all even.
        """
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)
