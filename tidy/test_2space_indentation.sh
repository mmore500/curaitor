#!/bin/bash
set -e

# enforce use of GNU version of coreutils
. ./tidy/util/enforce_gnu_utils.sh

TARGETS=$(find . -type f \( -name "*.hpp" -o -name "*.cpp" \) ! -path "./cpp/third-party/*" ! -path "./cpp/node_modules/*")

for filename in ${TARGETS}; do

  if grep -qE '^   ' "${filename}" && ! grep -qE '^  \S' "${filename}"; then
    echo "greater than 2-space indentation found in ${filename}"
    echo "(found 3+-space indentation without any exactly 2-space indents)"
    exit 1 # failure
  fi

done

exit 0 # success
