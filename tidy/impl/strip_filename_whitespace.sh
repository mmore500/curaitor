#!/bin/bash
set -e

# enforce use of GNU version of coreutils
. ./tidy/util/enforce_gnu_utils.sh

# enforce availability of dependencies
. ./tidy/util/enforce_dependency.sh rename

find ! -path "./cpp/third-party/*" ! -path "*/node_modules/*" -type d | grep '\s' | rename 's/\s/_/g'    # do the directories first
find ! -path "./cpp/third-party/*" ! -path "*/node_modules/*" -type f | grep '\s' | rename 's/\s/_/g'    # do the directories first
