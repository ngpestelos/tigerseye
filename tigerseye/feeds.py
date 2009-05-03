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

def load_from_dir(feed_dir, dbname):
    "Load previously saved feeds"
    for f in glob("%s/*.txt" % feed_dir):
        load_from_file(f, dbname)

def insert_feed(feed, entries, db):
    if feed.has_key('updated_parsed'):
        del feed['updated_parsed']
    feed['type'] = 'feed'
    for entry in entries:
        if entry.has_key('updated_parsed'):
            del entry['updated_parsed']
        if entry.has_key('published_parsed'):
            del entry['published_parsed']
    feed['entries'] = entries
    db.create(feed)

def load_from_file(filename='/n/data/feeds/feb4e15bb6c3095177b25c0127efdbeb39a6627e.txt', dbname='feeds'):
    "Extract entries from a file"
    d = feedparser.parse(file(filename))
    db = Server()[dbname]
    print d.entries[0]
    insert_feed(d.feed, d.entries, db)
