import random

def pick_sublist(items, size=1):
    itemcount = 0
    sublist = []
    if size < 0 or not items:
        return []

    while itemcount < size:
        sublist.append(items[random.randint(0, len(items)-1)])
        itemcount += 1

    return sublist
