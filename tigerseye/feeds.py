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

>>>> feeds.create_views('mydatabase')
"""

from citrine import parser
from couchdb import Server
import random, picker

def load_from_opml(filename, dbname):
    "Load feeds from OPML to a CouchDB database"
    outlines = parser.get_outlines(filename)
    db = Server()[dbname]
    for outline in outlines:
        load_outline(db, outline)

def load_outline(db, outline, ref=None):
    """Creates a Document for each outline.

    Stores reference information (i.e., outlines nested among other outlines)

    Checks first if the URL exists.
"""

    xmlUrl = outline.get('xmlUrl', '')
    title = outline.get('title', '')
    if feed_exists(db, xmlUrl, title):
        return

    htmlUrl = outline.get('htmlUrl', '')
    children = outline.get('outlines', [])
    row = {'text': outline.get('text', ''), 'title': title, \
      'feedtype': outline.get('type', ''), 'xmlUrl': outline.get('xmlUrl', ''), \
      'htmlUrl': outline.get('htmlUrl', ''), 'type': 'feed'}
    if ref:
        row['ref'] = ref
    docId = db.create(row)
    print "Loading outline from %s" % xmlUrl
    for child_outline in children:
        load_outline(db, child_outline, docId)

def delete_views(dbname):
    "Delete views related to feeds."
    db = Server()[dbname]
    del db['_design/feeds']

def create_views(dbname):
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
        },
        "titles": {
          "map": """function(doc) {
                      if (doc.type == 'feed')
                        emit([doc.title, doc._id], null);
                    }"""
        }
      }
    }
    db = Server()[dbname]
    db['_design/feeds'] = doc

def get_ids(dbname):
    "Return all Document IDs for feeds."
    db = Server()[dbname]
    return [r.key for r in db.view('feeds/ids')]

def get_urls(dbname):
    "Return all URLs for feeds."
    db = Server()[dbname]
    return [r.key for r in db.view('feeds/urls')]

def delete_all(dbname):
    "Remove all feed Documents"
    db = Server()[dbname]
    for id in get_ids(dbname):
        doc = db[id]
        print "Deleting %s" % doc['xmlUrl']
        db.delete(doc)

def get_random_url(dbname, size=1):
    "Returns a random list of URLs"
    urls = get_urls(dbname)
    return picker.pick_sublist(urls, size)

def feed_exists(db, url, title):
    "Checks the database if either the feed URL or feed title exists."
    urlfound = [r.key for r in db.view('feeds/urls', key=url)]
    titlefound = [r.key for r in db.view('feeds/titles', key=title)]
    if urlfound or titlefound:
        return True
    else:
        return False
