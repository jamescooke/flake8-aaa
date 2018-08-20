#!/bin/bash

set -eo pipefail

# ERROR CODES
# NO_ERROR=0
FATAL_MESSAGE=1
ERROR_MESSAGE=2
# WARNING_MESSAGE=4
# REFACTOR_MESSAGE=8
CONVENTION_MESSAGE=16
USAGE_ERROR=32

echo "> Raising on FATAL_MESSAGE, ERROR_MESSAGE, CONVENTION_MESSAGE, USAGE_ERROR"

set +e
pylint "$1"
lint_code=$?
set -e

(((lint_code&FATAL_MESSAGE)>0 || (lint_code&ERROR_MESSAGE)>0 || (lint_code&USAGE_ERROR)>0 || (lint_code&CONVENTION_MESSAGE)>0)) && exit $lint_code

exit 0
