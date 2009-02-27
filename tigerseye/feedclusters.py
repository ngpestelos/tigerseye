# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Nestor G Pestelos Jr
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

"""Strips words from saved feed entries.

   Based on code from Programming Collective Intelligence (Discovering Groups)
"""

import entries, stripper
from math import sqrt

def getwordcounts(dbname, id):
    feed_entries = entries.get_entries(dbname, id)
    wc = {}
    for e in feed_entries:
        words = stripper.getwords(e['description'])
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1

    return wc

def strip_all(dbname):
    apcount = {}
    wordcounts = {}
    feedlist = entries.get_ids(dbname)
    for id in feedlist:
        print id
        wc = getwordcounts(dbname, id)
        wordcounts[id] = wc
        for word, count in wc.items():
            apcount.setdefault(word, 0)
            if count > 1:
                apcount[word] += 1

    wordlist = []
    for w, bc in apcount.items():
        frac = float(bc) / len(feedlist)
        if frac > 0.1 and frac < 0.5: wordlist.append(w)

    return wordlist, wordcounts

def get_rownames(dbname, wordcounts):
    urls = entries.get_urls_by_id(dbname)
    id_urls = {}
    for id, url in urls:
        id_urls[id] = url
    return id_urls

def get_wordmatrix(wordlist, wordcounts):
    data = {}
    for id, wc in wordcounts.items():
        row = []
        for word in wordlist:
            if word in wc:
                row.append(wc[word])
            else:
                row.append(0)
        data[id] = row
    return data

def pearson(v1, v2):
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)
    
    # Sum of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * \
      (sum2Sq - pow(sum2, 2) / len(v2)))

    if den == 0: return 0

    return 1.0 - num / den

def get_rows(rownames, data):
    urls = []
    rows = []

    for id, url in rownames.items():
        urls.append(url)
        rows.append(data[id])

    return urls, rows

class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

    # Clusters are initially just the rows
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        # Loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                # distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = \
                        distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # calculate the average of the two clusters
        mergevec = [ \
          (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0 \
            for i in range(len(clust[0].vec))] 

        # create the new cluster
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]], \
          right=clust[lowestpair[1]], distance = closest, id = currentclustid)

        # cluster IDs that weren't in the original set are negative
        currentclustid =- 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]


def printcluster(clust, labels=None, n=0):
    # indent to make a hierarchy layout
    for i in range(n): print ' ',
    if clust.id < 0:
        # negative id means that this is a branch
        print '-'
    else:
        # positive id means that this is an endpoint
        if labels == None: print clust.id
        else: print labels[clust.id]

    # now print the left and right clusters
    if clust.left != None: printcluster(clust.left, labels, n = n+1)
    if clust.right != None: printcluster(clust.right, labels, n = n+1)        
