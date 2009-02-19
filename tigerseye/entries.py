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

def mark_as_failed(url):
    "Create a record indicating a problem on feed capture"
    pass

def delete_views(dbname='feeds'):
    "Delete views related to entries."
    db = Server()[dbname]
    del db['_design/entries']

def create_views(dbname='feeds'):
    "Create views for entries."
    doc = {
      "language": "javascript",
      "views": {
        "urls": {
          "map": """function(doc) {
                      if (doc.type == 'entries') emit(doc.link, null);
                    }"""
        },
        "by_url": {
          "map": """function(doc) {
                      if (doc.type == 'entries') emit(doc.link, doc);
                    }"""
        },
        "ids": {
          "map": """function(doc) {
                      if (doc.type == 'entries') emit(doc._id, null);
                    }"""
        }
      }
    }
    db = Server()[dbname]
    db['_design/entries'] = doc

def get_wordlist(url, dbname='feeds'):
    """Creates a word vector (frequency table of words) from the URL's entries.

    Strips out the HTML tags for each entry.

    Forms a large list by appending all the words for each entry.
    
    Create a table for word occurrences."""
    pass

def get_urls(dbname='feeds'):
    "Returns a list of URLs."
    db = Server()[dbname]
    return [r.key for r in db.view('entries/urls')]

def get_random_url(size=1, dbname='feeds'):
    "Returns a random list of URLs"
    urls = get_urls(dbname)
    urlcount = 0
    sublist = []
    if size < 0:
        return []
    while urlcount < size:
        # TODO: handle duplicate URLs
        sublist.append(urls[random.randint(0, len(urls))])
        urlcount += 1
    return sublist

def get_document(url, dbname='feeds'):
    "Return a Document for a URL. A Document may contain a list of entries."
    db = Server()[dbname]
    return [r.value for r in db.view('entries/by_url', key=url)][0]

def get_entries(url, dbname='feeds'):
    doc = get_document(url, dbname)
    return doc['entries']

def get_ids(dbname='feeds'):
    "Return a list of Document IDs."
    db = Server()[dbname]
    return [r.key for r in db.view('entries/ids')]

def load_from_dir(feed_dir, dbname='feeds'):
    """Import from a group of feed dumps.

    >>>> entries.load_from_dir('/path/to/dumps', 'feed_database')
    """
    def create_document(db, link, title, entries):
        print "Creating document for %s" % link
        stripped = []
        for e in entries:
            try:
                e1 = {'link': e['link'], \
                  'title': e['title'], 'description': \
                  e.get('description', '') or e.get('subtitle', '')}
            except:
                print "Unable to get entry %s" % e['link']
            else:
                stripped.append(e1)

        db.create({'type': 'entries', 'link': link, 'title': title, \
          'entries': stripped})

    for f in glob("%s/*.txt" % feed_dir):
        d = feedparser.parse(f)
        db = Server()[dbname]
        try:
            create_document(db, d.feed.link, d.feed.title, d.entries)
        except:
            print "Unable to parse %s" % f
