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
import hashlib, random

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
        "by_link": {
          "map": """function(doc) {
                      if (doc.type == 'entries') emit(doc.link, doc);
                    }"""
        },
        "by_id": {
          "map": """function(doc) {
                      if (doc.type == 'entries') emit(doc._id, doc);
                    }"""
        },
        "urls": {
          "map": """function(doc) {
                      if (doc.type == 'entries') emit(doc.link, null);
                    }"""
        }
      }
    }
    db = Server()[dbname]
    db['_design/entries'] = doc

def all(dbname='feeds'):
    db = Server()[dbname]
    return [r.key for r in db.view('entries/by_id')]

def get_urls(dbname='feeds'):
    db = Server()[dbname]
    return [r.key for r in db.view('entries/urls')]

def get_random_url(dbname='feeds'):
    "I'm feeling lucky."
    urls = get_urls(dbname)
    return urls[random.randint(0, len(urls))]

def get_document(url, dbname='feeds'):
    db = Server()[dbname]
    return [r.value for r in db.view('entries/by_link', key=url)][0]

def get_entries(url, dbname='feeds'):
    doc = get_document(url, dbname)
    return doc['entries']

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
