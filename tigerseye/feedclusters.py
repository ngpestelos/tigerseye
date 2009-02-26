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
