""" A module for capturing feed entries. 

    Creates a Document for each feed URL, with its list of entries.
"""
from glob import glob
import feedparser

def mark_as_failed(url):
    "Create a record indicating a problem on feed capture"
    pass

def load_from_dir(feed_dir):
    "Import from a group of feed dumps."
    def create_document(link, title, entries):
        print "creating doc"

    for f in glob("%s/*.txt" % feed_dir):
        d = feedparser.parse(f)
        link = ''
        title = ''
        try:
            link = d.feed.link
            title = d.feed.title
            entries = d.get('entries', [])
            if link:
                create_document(link, title, entries)
            else:
                print "Skipping %s" % f
        except:
            print "Unable to parse correctly: %s" % f

        #print d.entries[0]

load_from_dir('/n/data/feeds')
