#!/bin/bash

PYTHON_LIBRARY_DIRECTORIES="lib /usr/local/lib"

# Change to this script's directory
cd "$(dirname ${BASH_SOURCE[0]})"

PYTHON_VERSION=$(python -V 2>&1 | awk '{ print $2 }' | cut -d. -f 1-2)
PYTHON_VERSION_REGEX=$(echo $PYTHON_VERSION | sed 's/\./\\./g')

# echo $PYTHON_VERSION
# echo $PYTHON_VERSION_REGEX

# Install pyjade to the current directory
if [ ! -x bin/pyjade ]; then
    pip install --install-option="--prefix=$(pwd)" pyjade
fi

export PYTHONPATH=$(find $PYTHON_LIBRARY_DIRECTORIES -type d -name site-packages | grep "python${PYTHON_VERSION_REGEX}/" | xargs -n 1 ./get_path | tr '\n' ':' | sed 's/:$//')
