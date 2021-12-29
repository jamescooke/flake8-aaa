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

Then build py36 requirements:

.. code-block:: shell

    bv 3.6
    vvv
    pip install pip-tools
    cd requirements/
    make examples-py36.txt
