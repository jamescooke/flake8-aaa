#!/bin/bash

set -eo pipefail

# ERROR CODES
NO_ERROR=0
FATAL_MESSAGE=1
ERROR_MESSAGE=2
WARNING_MESSAGE=4
REFACTOR_MESSAGE=8
CONVENTION_MESSAGE=16
USAGE_ERROR=32

pylint flake8_aaa

((($$?&1)>0 || ($$?&2)>0 || ($$?&32)>0)) && echo "here"
