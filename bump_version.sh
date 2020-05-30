#!/bin/bash

# $ ./bump_version.sh [VERSION]
# Where:
#   [VERSION] current version string in "n.n.n" format, just numbers

set -eo pipefail

if [ -z "$1" ]; then
    echo "Please pass [VERSION]"
    exit 1
fi

# TODO check that no diff is being carried

new_version=$1

# --- Get current version ---

current_version="$(grep -Eo '^__version__.*$' src/flake8_aaa/__about__.py | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+')"
today=$(date "+%Y/%m/%d")

# TODO check that new version > current version

echo "Current version = '$current_version'"
echo "    New version = '$new_version'"
echo "          Today = '$today'"

# === Update __about__ ===

sed --in-place "s/__version__ = '$current_version'$/__version__ = '$new_version'/" src/flake8_aaa/__about__.py

echo "*** /src/flake8_aaa/__about__.py updated."

# === Update CHANGELOG ===

# Add new version subtitle after link to latest docs, released today

# underline=$(echo $new_version | sed 's/./-/g')
title="${new_version}_ - ${today}"
underline=${title//?/-}
sed --in-place "/#__unreleased_marker__/ a\ \n${title}\n${underline}" CHANGELOG.rst

# This leaves a single whitespace on the line above the new subtitle, so remove that

sed --in-place "s/^ $//" CHANGELOG.rst

# Update Unreleased link:

sed --in-place "s/^\.\. _Unreleased: .*$/.. _Unreleased: https:\/\/github.com\/jamescooke\/flake8-aaa\/compare\/v${new_version}...HEAD/" CHANGELOG.rst

# Add link for new release after unreleased link:

sed --in-place "/^\.\. _Unreleased: .*$/a .. _${new_version}: https://github.com/jamescooke/flake8-aaa/compare/v${current_version}...v${new_version}" CHANGELOG.rst

echo "*** /CHANGELOG.rst updated."
echo

git diff
