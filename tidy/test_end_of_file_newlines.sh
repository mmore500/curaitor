#!/bin/bash
set -e

# enforce use of GNU version of coreutils
. ./tidy/util/enforce_gnu_utils.sh

# refuse to continue if uncommitted changes are present
. ./tidy/util/enforce_git_status.sh

SOURCE_HASH=$( find -path ./cpp/third-party -prune -false -o -type f | sort | xargs cat | sha1sum )

./tidy/impl/ensure_end_of_file_newlines.sh

if [ "${SOURCE_HASH}" == "$( find -path ./cpp/third-party -prune -false -o -type f | sort | xargs cat | sha1sum )" ];
then
  exit 0 # success
else
  echo "missing end of file newlines detected, run ./tidy/impl/ensure_end_of_file_newlines.sh locally to find & fix"
  echo "why? see https://stackoverflow.com/a/729795"
  exit 1 # failure
fi
