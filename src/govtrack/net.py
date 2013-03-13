import gzip
import json
import networkx as nx

def writeobj(filename, obj):
    with gzip.open(filename, 'wb') as f:
        f.write(json.dumps(obj, indent=4))


def readobj(filename):
    with gzip.open(filename, 'r') as f:
        return json.loads(f.read())


def mkdict(obj, key='id'):
    return dict((x[key], x) for x in obj)


def cosponsors():
    'Return a graph of cosponsors'
    ret = nx.Graph()

    bills = mkdict(readobj('bills-113.json.gz'))
    people = mkdict(readobj('people.json.gz'))
    cosponsorships = readobj('cosponsorship.json.gz')

    for bill in cosponsorships:
        bill_id = bill['bill']
        if bill_id not in bills:
            continue

        author_id = bills[bill_id]['sponsor']['id']
        author = people[author_id]['name']
        cosponsor = people[bill['person']]['name']

        ret.add_edge(cosponsor, author)
    return ret
