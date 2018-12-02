#!/usr/bin/env python3

from collections import Counter

def checksum(ids):
    n_twice = 0
    n_thrice = 0

    for i in ids:
        c = Counter(i)
        n_twice += any(x == 2 for x in c.values())
        n_thrice += any(x == 3 for x in c.values())

    return n_twice * n_thrice

def find_close(ids):
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):

            count_not_matching = 0
            for x, y in zip(ids[i], ids[j]):
                if x!=y:
                    count_not_matching += 1
                    if count_not_matching > 1:
                        break
            else:
                if count_not_matching == 1:
                    return "".join(x for x, y in zip(ids[i], ids[j]) if x==y)

if __name__=="__main__":
    with open("02_inventory/input.txt", 'r') as f:
        ids = [x.strip() for x in f]

    print(checksum(ids))
    print(find_close(ids))
