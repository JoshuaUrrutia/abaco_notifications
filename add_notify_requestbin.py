import sys
import json
import re
import urlparse
import requests

from agavepy.agave import Agave
from requests.exceptions import HTTPError

system_id = sys.argv[1]
file_path = sys.argv[2]
events = '*'
assoc_ids = None
dest_uri = None


def get_requestbin():
    """Returns a temportary requestbin for API testing"""
    r = requests.post('https://requestbin.agaveapi.co/api/v1/bins')
    r.raise_for_status()
    body = r.json()
    name = body.get('name')
    return 'https://requestbin.agaveapi.co/' + name


try:
    ag = Agave.restore()
except HTTPError as h:
    raise h
except Exception as e:
    print("Unexpected error occurred: {}".format(e))

try:
    listing = ag.files.list(systemId=system_id,
                            filePath=file_path,
                            limit=1)[0]

    meta = listing['_links'].get('metadata', {})
    if 'href' in meta:
        muri = meta['href']
        parsed = urlparse.urlparse(muri)
        assoc_ids = urlparse.parse_qs(parsed.query)['q'][0].split(':')[1]
        assoc_ids = re.sub(r'[^.a-zA-Z0-9-]', '', assoc_ids)
        print('assocationIds = {}'.format(assoc_ids))
except HTTPError as h:
    raise h
except Exception as e:
    print("Unexpected error occurred: {}".format(e))

# Get a sample URI
try:
    dest_uri = get_requestbin()
except Exception as u:
    raise u

body = {'associatedUuid': assoc_ids,
        'event': '*',
        'url': dest_uri,
        'persistent': True}

try:
    resp = ag.notifications.add(body=json.dumps(body))
    if 'id' in resp:
        print('notification id: {}'.format(resp.get('id', '')))
        print('notification url: {}'.format(resp.get('url', '')))
except HTTPError as h:
    raise h
except Exception as e:
    print("Unexpected error occurred: {}".format(e))
