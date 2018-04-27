#!/bin/bash

set -eo pipefail

git fetch origin -v

branch_info=$(git status --short -b | head -1)

if [[ $branch_info != '## master...origin/master' ]]; then
    echo "Not on master or master not up to date with origin, branch = $branch_info"
    exit 1
fi
