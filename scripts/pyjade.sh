#!/bin/bash -e

#
# By sourcing this script, you will ensure that pyjade is installed,
# and available on the PYTHONPATH.
#

ORIG_PWD="$(pwd)"

PYTHON_LIBRARY_DIRECTORIES="lib /usr/local/lib"

# Change to this script's directory
cd "$(dirname ${BASH_SOURCE[0]})"

PYTHON_VERSION=$(python -V 2>&1 | awk '{ print $2 }' | cut -d. -f 1-2)
PYTHON_VERSION_REGEX=$(echo $PYTHON_VERSION | sed 's/\./\\./g')

# echo $PYTHON_VERSION
# echo $PYTHON_VERSION_REGEX

# Install pyjade to the current directory
if [ ! -d lib/pyjade ]; then
    # Workaround for a Homebrew bug that prevents "pip install --target" from working:
    # http://stackoverflow.com/questions/24257803/
    if [ ! -f ~/.pydistutils.cfg ]; then
    cat << EOF > ~/.pydistutils.cfg
[install]
prefix=
EOF
    fi
    pip install --target="$(pwd)/lib" pyjade
fi

# Previous version which used:
# pip install --install-option="--prefix=$(pwd)" pyjade
# (this doesn't handle dependencies)
#export PYTHONPATH=$(find $PYTHON_LIBRARY_DIRECTORIES -type d -name site-packages | grep "python${PYTHON_VERSION_REGEX}/" | xargs -n 1 ./get_path | tr '\n' ':' | sed 's/:$//')

export PYTHONPATH=$(./get_path lib)

cd "$ORIG_PWD"
