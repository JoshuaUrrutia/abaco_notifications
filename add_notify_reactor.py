import sys
import json
import re
#import urlparse
from urllib.parse import urlparse
from urllib.parse import parse_qs

from agavepy.agave import Agave
from requests.exceptions import HTTPError

system_id = sys.argv[1]
file_path = sys.argv[2]
actor_id = sys.argv[3]

events = '*'
assoc_ids = None
dest_uri = None

api_server = 'https://portals-api.tacc.utexas.edu/'
#api_server = 'https://agave.iplantc.org'
#api_server = 'https://api.sd2e.org'


def get_webhook(ag, actor_id):
    """
    Create a .actor.messages URI suitable for use in integrations
    """
    nonce_id = get_nonce(ag, actor_id)
    uri = '{}/actors/v2/{}/messages?x-nonce={}'.format(
        api_server, actor_id, nonce_id)
    return uri


def get_nonce(ag, actor_id):
    """Create a nonce for this actor"""
    body = {'level': 'EXECUTE', 'maxUses': -1}

    try:
        nonce = ag.actors.addNonce(actorId=actor_id,
                                   body=json.dumps(body))
        if 'id' in nonce:
            return nonce.get('id')
        else:
            raise ValueError('Invalid response from addNonce')
    except Exception as e:
        raise e


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
        parsed = urlparse(muri)
        assoc_ids = parse_qs(parsed.query)['q'][0].split(':')[1]
        assoc_ids = re.sub(r'[^.a-zA-Z0-9-]', '', assoc_ids)
        print('assocationIds = {}'.format(assoc_ids))
except HTTPError as h:
    raise h
except Exception as e:
    print("Unexpected error occurred: {}".format(e))

# Get a sample URI
try:
    dest_uri = get_webhook(ag, actor_id)
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
