#!/usr/bin/env python

import os
import sys

# Returns the number of whitespace characters in the string s
def get_leading_whitespace(s):
    return len(s) - len(s.lstrip())

# Returns the directory the current script (or interpreter) is running in
def get_script_directory():
    path = os.path.realpath(sys.argv[0])
    if os.path.isdir(path):
        return path
    else:
        return os.path.dirname(path)

os.chdir(get_script_directory())

def print_relevant_lines(filename):
    with open(filename) as f:
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

def main():
    print_relevant_lines('tmp/blueoaks.jade')

if __name__ == "__main__":
    main()
