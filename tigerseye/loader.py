# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Nestor G Pestelos Jr
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

"""Import a list of feeds to a couchdb database.

Requires couchdb-python.

>>>> from tigerseye import loader
>>>> loader.import_from_opml('myfeeds', 'google-reader-subscriptions.xml')
"""
from citrine import parser
from couchdb import Server
import hashlib

server = Server()

# Some outlines may have sub-outlines (children); store each outline
# as a document and put a reference to any parent
def import_outline(db, outline, ref=None):
    xmlUrl = outline.get('xmlUrl', '')
    htmlUrl = outline.get('htmlUrl', '')
    if xmlUrl:
        xmlHash = hashlib.sha1(xmlUrl).hexdigest()
    else:
        xmlHash = ''
    if htmlUrl:
        htmlHash = hashlib.sha1(htmlUrl).hexdigest()
    else:
        htmlHash = ''
    children = outline.get('outlines', [])
    row = {'text': outline.get('text', ''), 'title': outline.get('title', ''),\
        'type': outline.get('type', ''), 'xmlUrl': xmlUrl, 'htmlUrl': htmlUrl,\
        'xmlHash': xmlHash, 'htmlHash': htmlHash}
    if ref:
        row['ref'] = ref
    docId = db.create(row)
    for child_outline in children:
        import_outline(db, child_outline, ref=docId)

def import_from_opml(dbname, filename):
    outlines = parser.get_outlines(filename)
    db = server[dbname]
    for outline in outlines:
        import_outline(db, outline)
