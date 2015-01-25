#!/usr/bin/env python


index = 0
with open('sponsors2.txt') as f:
    text = ''
    url = ''
    for i, line in enumerate(f):
        if (i & 1):
            url = line.strip()
            print ("{text},{url}".format(text=text,url=url))
        else:
            text = line.strip()
