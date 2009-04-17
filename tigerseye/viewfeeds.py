from couchdb import Server

db = Server()['entries']

def _entries(feedurl):
    return [r.value for r in \
      db.view('_design/entries/_view/feeds', key=feedurl)]

def get_urls():
    dump = {}
    for r in db.view('_design/entries/_view/feed_urls'):
        dump[r.key] = 1
    return dump.keys()

def get_titles(feedurl):
    entrylist = _entries(feedurl)
    return [e['entryTitle'] for e in entrylist]

def get_contents(feedurl):
    entrylist = _entries(feedurl)
    return [e['description'] for e in entrylist]

if __name__ == '__main__':
    #entries = get_entries('http://21ccw.blogspot.com/')
    #print [e['description'] for e in entries]
    print get_titles('http://21ccw.blogspot.com/')
