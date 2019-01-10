#!/usr/bin/env python3

from itertools import product

def read(claim):
    claim_id, _, start, size = claim.split()
    x, y = (int(x) for x in start[:-1].split(','))
    w, h = (int(x) for x in size.split('x'))
    return int(claim_id[1:])-1, x, y, w, h

def process(claims, size=1000):
    # in grid, a number x means claimed by claim_id = x
    # -1 means already claimed by multiple people
    # None means as yet unclaimed
    grid = [[None]*size for _ in range(size)]

    overlapping_claim = [False]*len(claims)

    for claim_id, x, y, w, h in map(read, claims):
        for yi, xi in product(range(y, y+h), range(x, x+w)):

            if grid[yi][xi] is None:
                grid[yi][xi] = claim_id
            elif grid[yi][xi] == -1:
                overlapping_claim[claim_id] = True
            else:
                overlapping_claim[grid[yi][xi]] = True
                overlapping_claim[claim_id] = True
                grid[yi][xi] = -1

    return grid, overlapping_claim

def overlap(claims):
    grid, overlapping_claim = process(claims)

    part1 = sum(sum(x==-1 for x in row) for row in grid)

    part2 = overlapping_claim.index(False) + 1

    return part1, part2

if __name__=="__main__":
    with open("03_fabric_cutting/input.txt", 'r') as f:
        claims = [x.strip() for x in f]

    for x in overlap(claims):
        print(x)
