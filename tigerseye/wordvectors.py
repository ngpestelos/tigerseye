"""Build a frequency table of words in a feed.

Based on code from Programming Collective Intelligence (Discovering Groups)."""

import entries
from couchdb import Server
import re

def getwords(html):
    """Strips out markup from some text.

    Returns a list of words."""
    txt = re.compile(r'<[^>]+>').sub('', html)
    words = re.compile(r'\W*').split(txt)
    return [word.lower() for word in words if word != '']

def getwordcounts(url, dbname='feeds'):
    """Counts the occurrence of words found in each entry."""
    doc = entries.get_document(url, dbname)
    wc = {}
    for e in doc['entries']:
        words = getwords(e['description'])
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    return wc

def delete_views(dbname='feeds'):
    "Delete views related to entries"
    db = Server()[dbname]
    del db['_design/wordvectors']

def create_views(dbname='feeds'):
    "Create views for word vectors"
    doc = {
      "language": "javascript",
      "views": {
        "urls": {
          "map": """function(doc) {
                      if (doc.type == 'wordvector') emit(doc.link, null);
                    }"""
        }
      }
    }
    db = Server()[dbname]
    db['_design/wordvectors'] = doc

def save_counts(link, wc, dbname='feeds'):
    db = Server()[dbname]
    db.create({'link': link, 'type': 'wordvector', 'words': wc})

def get_urls(dbname='feeds'):
    db = Server()[dbname]
    return [r.key for r in db.view('wordvectors/urls')]

def delete_all(dbname='feeds'):
    "Delete all word vectors."
    for id in get_ids(dbname):

def strip_all(dbname='feeds'):
    "Strip all words from feeds."
    db = Server()[dbname]
    for id in entries.get_ids(dbname):
        doc = db[id]
        print "Stripping words from %s" % doc['link']
        wc = getwordcounts(doc['link'])
        save_counts(doc['link'], wc, dbname)
