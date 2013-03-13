from functools import wraps
import json
import requests
from urlparse import parse_qs, urljoin, urlsplit
import logging


def call(f):
    @wraps(f)
    def decorated(self, **kwargs):
        return self._call(f.__name__, **kwargs)
    return decorated


def call_by_path(f):
    @wraps(f)
    def decorated(self, arg):
        return self._call(f.__name__ + '/' + arg)
    return decorated

PAGE_SIZE = 600

class API(object):
    url = 'http://www.govtrack.us/api/v2/'

    def __init__(self):
        self.session = requests.session()

    def _call(self, endpoint, **params):
        limit = params.get('limit', None)
        if not limit:
            params['limit'] = PAGE_SIZE
        for k, v in params.iteritems():
            if not v:
                params.pop(k)
            elif isinstance(v, (list, tuple)):
                params[k + '[]'] = params.pop(k)

        url = urljoin(self.url, endpoint)
        result = self.session.get(url, params=params)
        print '# called ' + result.url
        try:
            result = json.loads(result.content)
        except:
            return None

        meta = result.pop('meta')

        total_pages = (meta['total_count'] / PAGE_SIZE) + 1
        if not limit and total_pages > 1:
            for page in range(1, total_pages):
                print "# fetching page %s" % page
                params['offset'] = page * PAGE_SIZE
                next_result = self.session.get(url, params=params)
                next_result = json.loads(next_result.content)

                result['objects'].extend(next_result['objects'])

        return result['objects']

    @call
    def bill(self, congress='113'):
        pass

    @call
    def cosponsorship(self):
        pass

    @call
    def person(self):
        pass
