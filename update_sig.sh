#!/bin/bash

set -eo pipefail

echo "Current:"
grep -E "CPython" README.rst

echo "Running tox to generate new line..."
NEWLINE=$(tox -e py36-install | grep -E "CPython")

echo "Updating file..."
sed -i "s/.* CPython .* Linux/    $NEWLINE/" README.rst

git diff -- README.rst
