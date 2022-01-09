AAA04: expected 1 blank line before Assert block, found none
------------------------------------------------------------

For tests that have an Assert block, there must be a blank line between the Act
and Assert blocks, but Flake8-AAA could not find one.

This blank line creates separation between the action and the assertions and
makes the Act block easy to spot.

As with rule ``AAA03``, this rule works best with ``E303`` enabled.

Resolution
..........

Add a blank line before the Assert block.
