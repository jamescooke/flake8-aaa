AAA02: multiple Act blocks found in test
----------------------------------------

There must be one and only one Act block in every test but Flake8-AAA found
more than one potential Act block. This error is usually triggered when a test
contains more than one ``result =`` statement or more than one line marked ``#
act``. Multiple Act blocks create ambiguity and raise this error code.

Resolution
..........

Split the failing test into multiple tests. Where there is complicated or
reused set-up code then apply the DRY principle and extract the reused code
into one or more fixtures.
