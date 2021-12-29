Requirements
============

Handling Python 3.6 needs some efforts (py36) when bumping requirements.

These are just notes for myself to maintain requirements.

When bumping everything, first build all the main requirements with latest
Python:

.. code-block:: shell

    bv 3.9
    vvv
    pip install pip-tools
    cd requirements/
    rm *.txt
    make

Then build py36 test and examples requirements:

.. code-block:: shell

    bv 3.6
    vvv
    pip install pip-tools
    cd requirements/
    make examples-py36.txt test-py36.txt

Notes
-----

* There are dev requirements that can not be installed in py36.

* py36 has its own test and example requirements.
