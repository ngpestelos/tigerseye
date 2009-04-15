# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Nestor G Pestelos Jr
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

""" A module for capturing feed entries. 

    Creates a Document for each feed URL, with its list of entries.
"""
from glob import glob
import feedparser
from couchdb import Server
import hashlib, random, re

def load_from_file(filename, dbname='entries'):
    "Extract entries from a file"
    def do_insert(docs):
        for entry in docs:
            try:
                db[entry['entryUrl']] = entry
            except:
                print "Failed to add entry"
                continue

    d = feedparser.parse(file(filename))
    db = Server()[dbname]
    try:
        docs = create_documents(db, d.feed.link, d.feed.title, d.entries)
    except:
        print "Unable to create documents for %s" % filename
    else:
        do_insert(docs)
 
def create_documents(db, link, title, entries):
    def make_doc(entry):
        return {'feedUrl': link, 'feedTitle': title, \
                'entryUrl': entry['link'], 'entryTitle': entry['title'], \
                'description': entry.get('description') or e.get('subtitle'), \
                'updated': entry['updated']}

    return [make_doc(e) for e in entries]

def load_from_dir(feed_dir, dbname='entries'):
    for f in glob("%s/*.txt" % feed_dir):
        load_from_file(f, dbname)
