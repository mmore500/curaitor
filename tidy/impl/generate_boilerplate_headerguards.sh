#!/bin/bash
set -e

# assumes docstring boilerplate is already in place

# enforce use of GNU version of coreutils
. ./tidy/util/enforce_gnu_utils.sh

for filename in $(cd cpp/include && find * -name '*.hpp' -type f); do

  GUARD=$( sed "s/[^[:alnum:]]/_/g" <<< "$filename" | tr "[:lower:]" "[:upper:]" )
  NDEF_LINE="#ifndef ${GUARD}_INCLUDE"
  DEF_LINE="#define ${GUARD}_INCLUDE"
  ENDIF_LINE="#endif // ${NDEF_LINE}"

  sed -i '1s/^.*$/'"#pragma once"'/' "cpp/include/${filename}"
  sed -i '2s/^.*$/'"${NDEF_LINE}"'/' "cpp/include/${filename}"
  sed -i '3s/^.*$/'"${DEF_LINE}"'/' "cpp/include/${filename}"
  sed -i '$ s,^.*$,'"${ENDIF_LINE}"',g' "cpp/include/${filename}"

done
