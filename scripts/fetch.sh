#!/bin/bash -e

# Change to this script's directory and create a tmp directory
cd "$(dirname $0)"
mkdir -p tmp

# Check if html2jade exists
if [ ! -x node_modules/.bin/html2jade ]; then
    npm install html2jade
fi

# Fetch the Blue Oaks web page
curl -s "http://www.rcsdk8.org/apps/pages/?uREC_ID=89894&type=d" > tmp/blueoaks.html

# Convert the Blue Oaks web page to jade format
# (a .jade file will be written alongside the .html file)
node_modules/.bin/html2jade tmp/blueoaks.html
