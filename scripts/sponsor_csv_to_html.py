#!/usr/bin/env python

import csv
import sys
from xml.sax.saxutils import escape

with open(sys.argv[1], 'r') as f:
    reader = csv.reader(f)
    platinum = []
    silver = []
    donations = []
    l = None

    for row in reader:
        if row[2].lower() == 'y':
            if row[3].lower() == 'platinum':
                l = platinum
            elif row[3].lower() == 'silver':
                l = silver
            elif row[3].lower() == 'donations':
                l = donations
            l.append('<h4><a href="http://{url}">{text}</a></h4>'.format(url=row[1],text=escape(row[0])))

    print ('Platinum:')
    for item in platinum: print (item)
    print ('')

    print ('Silver:')
    for item in silver: print (item)
    print ('')

    print ('Donations:')
    for item in donations: print (item)
