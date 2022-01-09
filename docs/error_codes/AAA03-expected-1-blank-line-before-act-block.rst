AAA03: expected 1 blank line before Act block, found none
---------------------------------------------------------

For tests that have an Arrange block, there must be a blank line between the
Arrange and Act blocks, but Flake8-AAA could not find one.

This blank line creates separation between the arrangement and the action and
makes the Act block easy to spot.

This rule works best with `pycodestyle
<https://pypi.org/project/pycodestyle/>`_'s ``E303`` rule enabled because it
ensures that there are not multiple blank lines between the blocks.

Resolution
..........

Add a blank line before the Act block.
