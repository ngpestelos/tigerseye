# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Nestor G Pestelos Jr
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

"""Import a list of feeds to a database.

>>>> from tigerseye import feeds
>>>> feeds.load_from_opml('my_opml_file.xml', 'mydatabase')
"""

from citrine import parser
from couchdb import Server
import random, picker

def load_from_opml(filename, dbname='feeds'):
    "Load feeds from OPML to a CouchDB database"
    outlines = parser.get_outlines(filename)
    db = Server()[dbname]
    for outline in outlines:
        load_outline(db, outline)

def load_outline(db, outline, ref=None):
    """Creates a Document for each outline.

    Stores reference information (i.e., outlines nested among other outlines)"""
    xmlUrl = outline.get('xmlUrl', '')
    htmlUrl = outline.get('htmlUrl', '')
    children = outline.get('outlines', [])
    row = {'text': outline.get('text', ''), 'title': outline.get('title', ''), \
      'feedtype': outline.get('type', ''), 'xmlUrl': outline.get('xmlUrl', ''), \
      'htmlUrl': outline.get('htmlUrl', ''), 'type': 'feed'}
    if ref:
        row['ref'] = ref
    docId = db.create(row)
    print "Loading outline from %s" % xmlUrl
    for child_outline in children:
        load_outline(db, child_outline, docId)

def delete_views(dbname='feeds'):
    "Delete views related to feeds."
    db = Server()[dbname]
    del db['_design/feeds']

def create_views(dbname='feeds'):
    "Create views for feeds."
    doc = {
      "language": "javascript",
      "views": {
        "urls": {
          "map": """function(doc) {
                      if (doc.type == 'feed') emit (doc.xmlUrl, null);
                    }"""
        },
        "ids": {
          "map": """function(doc) {
                      if (doc.type == 'feed') emit (doc._id, null);
                    }"""
        }
      }
    }
    db = Server()[dbname]
    db['_design/feeds'] = doc

def get_ids(dbname='feeds'):
    "Return all Document IDs for feeds."
    db = Server()[dbname]
    return [r.key for r in db.view('feeds/ids')]

def get_urls(dbname='feeds'):
    "Return all URLs for feeds."
    db = Server()[dbname]
    return [r.key for r in db.view('feeds/urls')]

def delete_all(dbname='feeds'):
    "Remove all feed Documents"
    db = Server()[dbname]
    for id in get_ids(dbname):
        doc = db[id]
        print "Deleting %s" % doc['xmlUrl']
        db.delete(doc)

def get_random_url(size=1, dbname='feeds'):
    "Returns a random list of URLs"
    urls = get_urls(dbname)
    return picker.pick_sublist(urls, size)
