#!/usr/local/bin/python

import os
import imaplib
from tidylib import tidy_document
import json

config_file = open(os.path.expanduser('~/.ccapi'))
config_data = json.load(config_file)
config_file.close()

username = config_data['imap_username']
password = config_data['imap_password']

from HTMLParser import HTMLParser
from urlparse import urlparse
from urlparse import parse_qs

def attr_dictionary(attrs):
    result = {}
    for attr in attrs:
        #print "(%s, %s)" % (attr[0], attr[1])
        result[attr[0]] = attr[1]
    #print result
    return result

class MyHTMLParser(HTMLParser):
    campaign_id = -1

    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag:", tag
        if tag == 'img':
            a = attr_dictionary(attrs)
            if 'src' in a:
                if a['src'].endswith('p1x1.gif'):
                    #print 'Found 1x1 image; href=%s' % a['src']
                    query = urlparse(a['src']).query

                    # This incantation finds the Constant Contact campaign ID,
                    # given their 1x1 tracking image URL
                    self.campaign_id = parse_qs(query)['t'][0].split('.')[0]
            
    def handle_endtag(self, tag):
        #print "Encountered an end tag :", tag
        pass
    def handle_data(self, data):
        #print "Encountered some data  :", data
        pass

    def get_campaign_id(self):
        return self.campaign_id


def process_message(data):
    import email
    import quopri
    m = email.message_from_string(data)
    if m.is_multipart():
        # XXX scan for correct content type?
        p = m.get_payload(1)
        out = quopri.decodestring(p.as_string())
        return out
    return None

imap = imaplib.IMAP4_SSL(config_data['imap_host'])
imap.login(username, password)
imap.select() # should select INBOX

imap.select()
typ, data = imap.search(None, 'ALL')
for num in data[0].split():
    typ, data = imap.fetch(num, '(RFC822)')
    #print 'Message %s\n%s\n' % (num, data[0][1])
    message = process_message(data[0][1])
    document, errors = tidy_document(message)
    #print document
    parser = MyHTMLParser()
    parser.feed(document)
    print "Campaign ID: ", parser.get_campaign_id()
    
imap.close()
imap.logout()
