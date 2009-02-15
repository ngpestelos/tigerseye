"""Design documents for pre-defined views.

Deletes any existing views before any creation takes place.
"""

from couchdb import Server

feeds_doc = {
  "language": "javascript",
  "views" : {
    "all" : {
      "map": """function(doc) { 
                  if (doc.xmlUrl || doc.htmlUrl) emit(doc._id, doc); 
                }"""
    },
    "xmlUrl": {
      "map": """function(doc) {
                  if (doc.xmlUrl) emit(doc.xmlUrl, doc);
                }"""
    },
    "xmlHash": {
      "map": """function(doc) {
                  if (doc.xmlHash) emit(doc.xmlHash, doc);
                }"""
    },
    "title": {
      "map": """function(doc) {
                  if (doc.title) emit([doc._id, doc.title], doc);
                }"""
    }
  }
}

def create(dbname):
    db = Server()[dbname]
    db['_design/feeds'] = feeds_doc

def delete(dbname):
    db = Server()[dbname]
    if db['_design/feeds']:
        del db['_design/feeds']

delete('feeds')
create('feeds')
