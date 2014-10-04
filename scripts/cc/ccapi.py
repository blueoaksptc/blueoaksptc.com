#!/usr/local/bin/python

import os
import sys
import requests
import json
#from tidylib import tidy_document
import logging
import time


config_file = open(os.path.expanduser('~/.ccapi'))
config_data = json.load(config_file)
config_file.close()

# globals
g_client = requests.session()
g_api_key = config_data['api_key']
g_bearer_auth = config_data['bearer_auth']
g_constant_contact_api = 'https://api.constantcontact.com/v2/%s'

g_relevant_list_name = '14-15 E-mail List'
g_relevant_list_id = 0

def modified_since_this_school_year():
    from datetime import date
    today = date.today()

    if today.month < 7:
        year = today.year - 1
    else:
        year = today.year

    modified_since = '%d-%02d-%02d' % (year, 07, 01)
    return modified_since


def configure_logging(verbose=False):
    logging.basicConfig()
    if verbose:
        import httplib
        httplib.HTTPConnection.debuglevel = 1
        logging.getLogger().setLevel(logging.DEBUG)

        # enable debugging at httplib level (requests->urllib3->httplib)
        # you will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
        # the only thing missing will be the response.body which is not logged.
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True


def set_arguments(**params):
    params['api_key'] = g_api_key
    return params


def request(uri, **params):
    campaigns_uri = g_constant_contact_api % uri
    g_client.headers = {
            "Authorization": "Bearer %s" % g_bearer_auth,
            "Content-Type": "application/json"
        }

    g_client.params = set_arguments(**params)
    response = g_client.get(campaigns_uri)
    data = response.json()
    time.sleep(.25) # the API only allows 4 requests per second
    return data


def request_campaign(id):
    data = request("emailmarketing/campaigns/%s" % id)
    return data


def request_campaign_preview(id):
    data = request("emailmarketing/campaigns/%s/preview" % id)
    return data


def print_campaign_preview(id):
    data = request_campaign_preview(id)
    print json.dumps(data, indent=4)

    from tidylib import tidy_document
    document, errors = tidy_document(data['preview_email_content'])
    logging.debug("HTML preview:")
    logging.debug(document.encode('utf-8'))
    logging.debug("Text preview")
    logging.debug(data['preview_text_content'].encode('utf-8'))


def main():
    configure_logging(verbose=False)

    data = request("lists")
    #print json.dumps(data, indent=4)

    for list in data:
        if(list['name'] == g_relevant_list_name):
            g_relevant_list_id = list['id']
            logging.debug("Got e-mail list; name=\"{name}\", id={id} ".format(name=g_relevant_list_name, id=g_relevant_list_id))

    data = request("emailmarketing/campaigns",
                   modified_since=modified_since_this_school_year(),
                   status='SENT')
    print json.dumps(data, indent=4)

    campaigns = []
    for result in data['results']:
        campaigns.append(result['id'])

    #data = request_campaign(1118693304123)
    #print json.dumps(data, indent=4)

    for campaign in campaigns:
        data = request_campaign(campaign)
        for contact_list in data['sent_to_contact_lists']:
            if g_relevant_list_id == contact_list['id']:
                print "Campaign[{cid}]: {subject}".format(cid=data['id'], subject=data['subject'])
                print "Permalink URL: {url}".format(url=data['permalink_url'])
                for link in data['click_through_details']:
                    print "  Link[{id}] count={count} {url}".format(id=link['url_uid'], count=link['click_count'], url=link['url'])
                #print json.dumps(data, indent=4)
                print ""

    #print_campaign_preview(1118693304123)



if __name__ == '__main__':
    main()