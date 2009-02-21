# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Nestor G Pestelos Jr
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

"""Build a frequency table of words for each feed.

Based on code from Programming Collective Intelligence (Discovering Groups)
"""

from couchdb import Server
import entries, stripper

def strip_all(dbname='feeds'):
    "Strip all words from feeds with entries."
    db = Server()[dbname]
    for id in entries.get_ids(dbname):
        doc = db[id]
        print "Stripping words from %s" % doc['link']
        entrywords = {}
        for e in doc['entries']:
            wc = stripper.getwordcounts(e['description'])
            entrywords[e['title']] = wc
        save(db, doc['link'], entrywords)

def save(db, url, vectors):
    db.create({'url': url, 'words': vectors, 'type': 'feedvectors'})

def delete_views(dbname='feeds'):
    "Delete feed vector views."
    db = Server()[dbname]
    del db['_design/feedvectors']

def create_views(dbname='feeds'):
    "Create views for feed vectors."
    doc = {
      "language": "javascript",
      "views": {
        "all": {
          "map": """function(doc) {
                      if (doc.type == 'feedvectors') emit(doc.url, doc);
                    }"""
        }
      }
    }
    db = Server()[dbname]
    db['_design/feedvectors'] = doc
