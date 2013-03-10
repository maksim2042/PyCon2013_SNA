desc = '''
People API
The people API is used to query the system for individuals, or groups of people matching given criteria. The following describes the parameters that can be used.
First Name (first_name)
Specify the first name of the person
http://api.opencongress.org/people?first_name=John
Last Name (last_name)
Specify the last name of the person
http://api.opencongress.org/people?last_name=Kerry
OpenCongress ID (person_id)
Specify the id of the person
http://api.opencongress.org/people?person_id=300056
Gender (gender)
Specify the gender of the person, either 'M' or 'F'
http://api.opencongress.org/people?gender=M&last_name=Kennedy
State (state)
Specify the two letter state of the person
http://api.opencongress.org/people?first_name=John&state=AZ
District (district)
Specify the congressional district of the person
http://api.opencongress.org/people?district=1&state=FL
Party (party)
Specify the political party of the person, either 'Republican', 'Democrat', or 'Independent'
http://api.opencongress.org/people?party=Republican&state=FL
User Approval Range (user_approval_from, user_approval_to)
Specify an average OpenCongress user approval rating range (0.0 to 10.0)
http://api.opencongress.org/people?user_approval_from=5.0&user_approval_to=10.0
Senators most in the news this week
http://api.opencongress.org/senators_most_in_the_news_this_week
Representatives most in the news this week
http://api.opencongress.org/representatives_most_in_the_news_this_week
Most blogged Senators this week
http://api.opencongress.org/most_blogged_senators_this_week
Most blogged Representatives this week
http://api.opencongress.org/most_blogged_representatives_this_week
Compare Two People
Specify the ID's of two people to compare, and receive XML of their roll call vote comparisons.
http://api.opencongress.org/person/compare.xml?person1=300001&person2=300013
People Approved of by Open Congress Users are Also
Returns bills, representatives, and senators supported and opposed by users's approving of a given person.
http://api.opencongress.org/opencongress_users_supporting_person_are_also/300060
People Disapproved of by Open Congress Users are Also
Returns bills, representatives, and senators supported and opposed by users's disapproving of a given person.
http://api.opencongress.org/opencongress_users_opposing_person_are_also/300060
Open Congress Users tracking person are also tracking
Returns bills, people, and issues commonly tracked by people tracking a given person.
http://api.opencongress.org/opencongress_users_tracking_person_are_also_tracking/300060
Bills API
The Bills API is used to query OpenCongress for bills matching given criteria. The following describes the functions and parameters that can be used.
Bills by session of congress
Returns bills matching the given congress.
http://api.opencongress.org/bills?congress=113
Bills by type
Returns bills matching the given type. Type can be: h (house), s (senate), hj (house joint resolution), sj (senate joint resolution), hc (house concurrent resolution) sc (senate concurrent resolution), hr (house resolution), sr (senate resolution)
http://api.opencongress.org/bills?type=h&congress=113
Bills by number
Returns bills matching the given number.
http://api.opencongress.org/bills?number=5749&type=h&congress=113
Bills by ident
Returns bills matching the given OpenCongress identification strings (session + chamber + bill number).
http://api.opencongress.org/bills_by_ident?ident[]=110-s1178&ident[]=110-s239
Bills Introduced Since
Returns bills that were introduced since the supplied date (30 at a time).
http://api.opencongress.org/bills_introduced_since?date=Jan 30th, 2009
Bills by Query
Returns bills matching a text query.
http://api.opencongress.org/bills_by_query?q=Global Poverty Act of 2007
Hot Bills
Returns bills that OpenCongress editors feel are "hot".
http://api.opencongress.org/hot_bills
Stalled Bills
Returns bills that have passed one chamber but have not received a vote on passage in the other (or a conference vote).
http://api.opencongress.org/stalled_bills?session=113&passing_chamber=s
Most Blogged Bills this Week
Returns the most bills most blogged about this week.
http://api.opencongress.org/most_blogged_bills_this_week
Bills Most in the News this Week
Returns the most bills most reported on by news agencies this week.
http://api.opencongress.org/bills_in_the_news_this_week
Most Commented-On Bills This Week
Returns 20 bills with the most comments added in the last week.
http://api.opencongress.org/most_commented_this_week
Most Tracked Bills this Week
Returns the most bills most tracked by OpenCongress Users this week.
http://api.opencongress.org/most_tracked_bills_this_week
Most Supported Bills this Week
Returns the most bills most supported by OpenCongress Users this week.
http://api.opencongress.org/most_supported_bills_this_week
Most Opposed Bills this Week
Returns the most bills most opposed by OpenCongress Users this week.
http://api.opencongress.org/most_opposed_bills_this_week
Bills Supported by Open Congress Users are Also
Returns bills, representatives, and senators supported and opposed by users's supporting a given bill.
http://api.opencongress.org/opencongress_users_supporting_bill_are_also/111-s1
Bills Opposed by Open Congress Users are Also
Returns bills, representatives, and senators supported and opposed by users's opposing a given bill.
http://api.opencongress.org/opencongress_users_opposing_bill_are_also/111-s1
Open Congress Users tracking bill are also tracking
Returns bills, people, and issues commonly tracked by people tracking a given bill.
http://api.opencongress.org/opencongress_users_tracking_bill_are_also_tracking/111-s1
Roll Calls
Roll Calls by Bills
Returns the roll calls for a given list of bills.
http://api.opencongress.org/bill_roll_calls?bill_id[]=51865&bill_id[]=51868
Issues
Issues by Keyword
Specify a Keyword, and receive an array of issue areas that match the keyword.
http://api.opencongress.org/issues_by_keyword?keyword=Privacy
'''

from functools import wraps
import json
import requests
from urlparse import parse_qs, urljoin, urlsplit
import logging

urls = (x.strip() for x in desc.split('\n') if x.startswith('http'))


def print_methods():
    funs = {}
    # Construct function signatures
    for url in urls:
        url = urlsplit(url)
        path = url.path.strip('/')
        fun, _, arg = path.partition('/')
        fundict = funs.setdefault(fun, {})
        if arg:
            fundict['arg'] = arg
            continue
        else:
            parsed = parse_qs(url.query)
            for name, value in parsed.iteritems():
                if '[]' not in name:
                    fundict[name] = value[0]
                else:
                    # name = name.replace('[]', '')
                    fundict.setdefault(name, []).extend(value)

    for f, desc in sorted(funs.iteritems()):
        args = ['%s=%r'%x for x in desc.items()]
        if args:
            args = [''] + args
        print 'def %s(self%s):' % (f,
                                   ', '.join(args).replace('[]', ''))
        print '    return self._call(%s, %s)'
        print


def call(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        if arg:
            if not args:
                raise Exception("Need at least one arg")
            kwargs[arg] = args
        return self._call(f.__name__, **kwargs)
    return decorated


def call_by_path(f):
    @wraps(f)
    def decorated(self, arg):
        return self._call(f.__name__ + '/' + arg)
    return decorated


class API(object):
    url = 'http://api.opencongress.org/'

    def __init__(self):
        self.session = requests.session()

    def _call(self, endpoint, **params):
        params['format'] = 'json'
        for k, v in params.iteritems():
            if not v:
                params.pop(k)
            elif isinstance(v, (list, tuple)):
                params[k + '[]'] = params.pop(k)
        result = self.session.get(urljoin(self.url, endpoint), params=params)
        print 'called ' + result.url
        try:
            return json.loads(result.content)
        except:
            return None

    @call
    def bill_roll_calls(self, *bill_ids):
        # =['51865', '51868']):
        return self._call('bill_roll_calls', bill_id=bill_ids)

    @call
    def bills(self, type='h', number='5749', congress='113'):
        pass

    @call
    def bills_by_ident(self, *ident):
        # =['110-s1178', '110-s239']):
        return self._call('bills_by_ident', ident=ident)

    def bills_by_query(self, q='Global Poverty Act of 2007'):
        return self._call('bills_by_query', q=q)

    @call
    def bills_in_the_news_this_week(self):
        pass

    @call
    def bills_introduced_since(self, date='Jan 30th, 2009'):
        pass

    @call
    def hot_bills(self):
        pass

    def issues_by_keyword(self, keyword='Privacy'):
        return self._call('issues_by_keyword', keyword=keyword)

    @call
    def most_blogged_bills_this_week(self):
        pass

    @call
    def most_blogged_representatives_this_week(self):
        pass

    @call
    def most_blogged_senators_this_week(self):
        pass

    @call
    def most_commented_this_week(self):
        pass

    @call
    def most_opposed_bills_this_week(self):
        pass

    @call
    def most_supported_bills_this_week(self):
        pass

    @call
    def most_tracked_bills_this_week(self):
        pass

    @call_by_path
    def opencongress_users_opposing_bill_are_also(self, bill='111-s1'):
        pass

    @call_by_path
    def opencongress_users_opposing_person_are_also(self, person_id='300060'):
        pass

    @call_by_path
    def opencongress_users_supporting_bill_are_also(self, bill='111-s1'):
        pass

    @call_by_path
    def opencongress_users_supporting_person_are_also(self, person_id='300060'):
        pass

    @call_by_path
    def opencongress_users_tracking_bill_are_also_tracking(self, bill='111-s1'):
        pass

    @call_by_path
    def opencongress_users_tracking_person_are_also_tracking(self, person_id='300060'):
        pass

    @call
    def people(self,
               first_name='John',
               last_name='Kennedy',
               district='1',
               gender='M',
               user_approval_from='5.0',
               state='FL',
               user_approval_to='10.0',
               person_id='300056',
               party='Republican'):
        pass

    def person_compare(self, person1=300001, person2=300013):
        return self._call('person/compare.xml', person1=person1, person2=person2)

    @call
    def representatives_most_in_the_news_this_week(self):
        pass

    @call
    def senators_most_in_the_news_this_week(self):
        pass

    @call
    def stalled_bills(self, passing_chamber='s', session='113'):
        pass
