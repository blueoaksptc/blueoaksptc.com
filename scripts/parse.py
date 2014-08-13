#!/usr/bin/env python

import os
import sys

def get_leading_whitespace(s):
    return len(s) - len(s.lstrip())

def get_script_directory():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

os.chdir(get_script_directory())

with open('tmp/blueoaks.jade') as f:
    lines = f.readlines()
    index = 0
    start_index = -1
    for line in map(str.strip, lines):
        # print line
        if line == 'ul.fbList':
            start_index = index
            break
        index = index + 1
    # print "Found start index: ", start_index
    lines = lines[start_index:]
    # print lines
    starting_whitespace = get_leading_whitespace(lines[0])
    index = 1
    for line in lines[1:]:
        if get_leading_whitespace(line) <= starting_whitespace:
            break
        index = index + 1
    # print "Found end index: ", index
    lines = lines[0:index]
    for line in lines:
        print line.rstrip()[starting_whitespace:]
