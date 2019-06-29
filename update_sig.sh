#!/bin/bash

set -eo pipefail

echo "Current:"
grep -E "CPython" README.rst

echo "Running tox to generate new line..."
NEWLINE=$(tox -e py36-install | grep -E "CPython")

echo "NEWLINE is \"$NEWLINE\""

VERSION=$(echo "$NEWLINE" | grep -Eo "aaa: [^,]*")

echo "Updating file..."
sed -i "s/.* CPython .* Linux/    $NEWLINE/" README.rst
sed -i "s/\`\`aaa: .*\`\`/\`\`$VERSION\`\`/" README.rst

git diff -- README.rst
