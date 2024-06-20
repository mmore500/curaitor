#!/bin/bash
set -e

# enforce use of GNU version of coreutils
. ./tidy/util/enforce_gnu_utils.sh

# enforce availability of dependencies
. ./tidy/util/enforce_dependency.sh rename

find ! -path "./cpp/third-party/*" ! -path "./.git/*" -type f | rename 's/\.h$/.hpp/'
find ! -path "./cpp/third-party/*" ! -path "./.git/*" -type f | rename 's/\.c$/.cpp/'
find ! -path "./cpp/third-party/*" ! -path "./.git/*" -type f | rename 's/\.cc$/.cpp/'
