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
