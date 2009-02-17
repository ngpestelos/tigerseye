# -*- coding: utf-8 -*-

""" A module for capturing feed entries. 

    Creates a Document for each feed URL, with its list of entries.
"""
from glob import glob
import feedparser
from couchdb import Server
import hashlib

def mark_as_failed(url):
    "Create a record indicating a problem on feed capture"
    pass

def load_from_dir(feed_dir, dbname='feeds'):
    "Import from a group of feed dumps."

    def create_document(db, link, title, entries):
        print "Creating document for %s" % link
        stripped = []
        for e in entries:
            try:
                e1 = {'link': e['link'], \
                  'title': e['title'], 'description': \
                  e.get('description', '') or e.get('subtitle', '')}
                stripped.append(e1)
            except:
                print "Problem with entry %s" % e['link']
        
        db.create({'type': 'entries', 'link': link, 'title': title, \
          'entries': stripped})

    for f in glob("%s/*.txt" % feed_dir):
        d = feedparser.parse(f)
        db = Server()[dbname]
        try:
            create_document(db, d.feed.link, d.feed.title, d.entries)
        except:
            print "Problem with feed %s" % f

load_from_dir('/n/data/feeds')
