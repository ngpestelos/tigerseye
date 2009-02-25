# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 Nestor G Pestelos Jr
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

"""Removes markup tags and splits words.

   Based on code from Programming Collective Intelligence
"""

import re

stopwords = ['and', 'or', 'the', 'a', 'of', 'to', 'in', 'is', 'it', 'for', \
  'at', 'on', 'with', 'which', 'this', 'that', 'as', 'be']

def getwords(html):
    """Strips out markup from some text.

    Returns a list of words.
    """
    txt = re.compile(r'<[^>]+>').sub('', html)
    words = re.compile(r'\W*').split(txt)
    lowercase = [word.lower() for word in words if len(words) > 1]
    return [w for w in lowercase if w not in stopwords]

def getwordcounts(txt):
    """Count the number of words in a string.

    Returns a table of words with their frequency."""
    wc = {}
    words = getwords(txt)
    for word in words:
        wc.setdefault(word, 0)
        wc[word] += 1
    return wc
