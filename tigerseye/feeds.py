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
    db = Server()[dbname]
    for f in glob("%s/*.txt" % feed_dir):
        load_from_file(f, db)

def remove_tuples(feed, entries):
    if feed.has_key('updated_parsed'):
        del feed['updated_parsed']
    for entry in entries:
        if entry.has_key('updated_parsed'):
            del entry['updated_parsed']
        if entry.has_key('published_parsed'):
            del entry['published_parsed']
    return feed, entries

def insert_feed(feed, entries, db):
    feed['type'] = 'feed'
    feed, entries = remove_tuples(feed, entries)
    feed['entries'] = entries
    try:
        db.create(feed)
    except:
        print "Could not load", feed.get('link', feed.get('title', ''))

def load_from_file(filename, db):
    "Extract entries from a file"
    d = feedparser.parse(file(filename))
    print "Processing", d.feed.get('link', d.feed.get('title', ''))
    insert_feed(d.feed, d.entries, db)
