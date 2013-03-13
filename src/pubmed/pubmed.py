#!/usr/bin/env python
# encoding: utf-8
"""
pubmed.py

Created by Maksim Tsvetovat on 2013-01-14.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from Bio import Entrez
from Bio import Medline
import progressbar
import simplejson as json

import matplotlib.pyplot as plot
import networkx as net
from utils import *

import dateutil.parser as parser
import datetime
import community
from itertools import permutations

Entrez.email = "maksim@tsvetovat.org"     # Always tell NCBI who you are

def make_pbar(maxval, text="Something"):
    widgets = [text+': ', progressbar.Percentage(), ' ', progressbar.Bar(marker=progressbar.RotatingMarker()),
               ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=maxval).start()
    return pbar

def get_number_of_records(term):
    handle = Entrez.egquery(term=term)
    record = Entrez.read(handle)
    for row in record["eGQueryResult"]:
        if row["DbName"]=="pubmed":
             return(row["Count"])

def get_article_ids(term):
    num_records=get_number_of_records(term)
    handle = Entrez.esearch(db="pubmed", term=term, retmax=num_records)
    record = Entrez.read(handle)
    idlist = record["IdList"]
    return idlist

def get_articles(term):
    idlist = get_article_ids(term)
    counter=0
    #pbar = make_pbar(len(idlist),text="Fetching")
    
    articles=[]
    if len(idlist) > 100:
        chunks=[idlist[i:i+100] for i in range(0, len(idlist), 100)]
        for chunk in chunks:
            handle = Entrez.efetch(db="pubmed", id=chunk, rettype="medline", retmode="text")
            articles.extend(list(Medline.parse(handle)))
            print '#'
            #pbar.update(p.currval+len(chunk))
    else:
        handle=Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode="text")
        articles.extend(list(Medline.parse(handle)))
    #pbar.finish()
    
    return articles
    
    
def make_author_network(articles):
    au_net=net.Graph()
    for article in articles:
        try:
            authors=article['AU']
        except KeyError:
            continue
        
        for a,b in permutations(authors, 2):
            add_or_inc_edge(au_net,a,b)
    return au_net
    
                
    
