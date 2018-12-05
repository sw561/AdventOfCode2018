#!/usr/bin/env python3

from collections import defaultdict, Counter
from itertools import combinations

def checksum(ids):
    n_twice = 0
    n_thrice = 0

    for i in ids:
        c = Counter(i)
        n_twice += 2 in c.values()
        n_thrice += 3 in c.values()

    return n_twice * n_thrice

def close(ids, i, j, N, second=False):
    if second:
        r = range(N//2, N)
    else:
        r = range(N//2)

    count_not_matching = 0
    for k in r:
        if ids[i][k] != ids[j][k]:
            count_not_matching += 1
            if count_not_matching > 1:
                return False
    return count_not_matching == 1

def find_close(ids):
    # If two ids match with the exception of exactly one letter, either the
    # first half matches exactly or the second half matches exactly.
    #
    # make two dicts, one for first halves and one for second halves.
    #
    # For each dict entry store list of indices for which ids[i] match in the
    # corresponding half

    first = defaultdict(list)
    second = defaultdict(list)
    N = len(ids[0])

    for i, x in enumerate(ids):
        first [x[:N//2]].append(i)
        second[x[N//2:]].append(i)

    for d, compare_second in zip([first, second], [True, False]):
        for candidate_indices in d.values():
            for i, j in combinations(candidate_indices, 2):
                if close(ids, i, j, N, second=compare_second):
                    return "".join(x for x, y in zip(ids[i], ids[j]) if x==y)

if __name__=="__main__":
    with open("02_inventory/input.txt", 'r') as f:
        ids = [x.strip() for x in f]

    print(checksum(ids))
    print(find_close(ids))
