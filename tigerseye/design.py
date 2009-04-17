from couchdb import Server

doc = {
  'language' : 'javascript',
  'views' : {
    'feeds'       : { 'map' : 'function(doc) { emit(doc.feedUrl, doc); }' },
    'feed_urls'   : { 'map' : 'function(doc) { emit(doc.feedUrl, null); }' }
  }
}

def load():
    db = Server()['entries']
    if db.get('_design/entries'):
        _doc = db['_design/entries']
        db.delete(_doc)
    db['_design/entries'] = doc

if __name__ == '__main__':
    load()
