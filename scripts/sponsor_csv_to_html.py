#!/usr/bin/env python

import csv
import sys

with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print ('<h4><a href="http://{url}">{text}</a></h4>'.format(url=row[1],text=row[0]))
