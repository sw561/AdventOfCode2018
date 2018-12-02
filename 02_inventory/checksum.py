#!/usr/bin/env python3

from collections import Counter
from itertools import combinations

def checksum(ids):
    n_twice = 0
    n_thrice = 0

    for i in ids:
        c = Counter(i)
        n_twice += 2 in c.values()
        n_thrice += 3 in c.values()

    return n_twice * n_thrice

def close(a, b):
    count_not_matching = 0
    for x, y in zip(a, b):
        if x!=y:
            count_not_matching += 1
            if count_not_matching > 1:
                return False
    return count_not_matching == 1

def get_candidate_combinations(ids, brute=False):

    if brute:
        # This is roughly the same speed for my input, but is likely to be
        # slower for an arbitrary list of id strings
        yield from combinations(ids, 2)
        return

    # Use a property of ids to sort, and thus avoid checking every pair of ids
    ids = [(sum(map(ord, x)), x) for x in ids]
    ids.sort()

    # Two ids which differ by more than 25 cannot be 'close'
    for i, (ha, a) in enumerate(ids):
        for hb, b in ids[i+1:]:
            if abs(hb - ha) > 25:
                break
            yield a, b

def find_close(ids):
    # Use a property of ids to sort, and thus avoid checking every pair of ids
    for a, b in get_candidate_combinations(ids):
        if close(a, b):
            return "".join(x for x, y in zip(a, b) if x==y)

if __name__=="__main__":
    with open("02_inventory/input.txt", 'r') as f:
        ids = [x.strip() for x in f]

    print(checksum(ids))
    print(find_close(ids))
