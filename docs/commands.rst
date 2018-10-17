Controlling flake8-aaa in-code
******************************

flake8-aaa can be controlled using some special comments in
your test code.

Explicitly marking blocks
=========================

One can set the act block explicitly using the ``# act``
comment. This is necessary when there is no assignment
possible.

Disabling flake8-aaa selectively
================================

When flake8-aaa finds the ``# noqa`` comment after the 
function/method head it will ignore this function/method.


