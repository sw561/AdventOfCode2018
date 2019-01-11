#!/usr/bin/env python3

import re
from itertools import product
from heapq import heappop, heappush

def read(fname):
    pattern = re.compile("-?\d+")
    with open(fname, 'r') as f:
        nanobots = [tuple(map(int, re.findall(pattern, line))) for line in f]

    return nanobots

def strongest(nanobots):
    return max(range(len(nanobots)), key=lambda x: nanobots[x][3])

def manhattan_distance(p1, p2):
    return sum(abs(p1i - p2i) for p1i, p2i in zip(p1, p2))

def count_in_range(nanobots, pos, r):
    return sum(manhattan_distance(bot[:3], pos) <= r for bot in nanobots)

def part1(nanobots):
    s = strongest(nanobots)
    pos = nanobots[s][:3]
    r = nanobots[s][3]
    return count_in_range(nanobots, pos, r)

def subcubes(min_coords, max_coords):
    # Yield 8 smaller cubes

    mid = [(left + right) // 2 for left, right in zip(min_coords, max_coords)]

    for p in product(range(2), repeat=3):
        mi = tuple(m if pi else left for pi, left, m in\
            zip(p, min_coords, mid)
            )
        ma = tuple(right if pi else m for pi, m, right in\
            zip(p, mid, max_coords)
            )
        yield mi, ma

def distance(left, right, x):
    if x < left:
        return left - x
    elif x >= right:
        return x - (right - 1)
    return 0

def in_range(min_coords, max_coords, x, y, z, r):
    d = sum(distance(l, r, u) for l, r, u in\
        zip(min_coords, max_coords, [x, y, z]))
    return d <= r

def count_in_range_cube(min_coords, max_coords, nanobots):
    return sum(in_range(min_coords, max_coords, *bot) for bot in nanobots)

def part2(nanobots):
    min_coords = tuple(min(bot[i] for bot in nanobots) for i in range(3))
    max_coords = tuple(max(bot[i] for bot in nanobots) for i in range(3))

    count = count_in_range_cube(min_coords, max_coords, nanobots)
    h = [(-count, min_coords, max_coords)]

    # Optimal will contain (-count, distance_from_origin)
    # Minimize this, to maximise count
    optimal = (0, 0)

    while h:
        mcount, min_coords, max_coords = heappop(h)

        if mcount > optimal[0]:
            return optimal[1]

        # print("Searching from {} {} {}".format(min_coords, max_coords, mcount))
        for sub in subcubes(min_coords, max_coords):
            if any(l == r for l, r in zip(*sub)):
                # This is a zero volume cube, no need to consider it
                continue

            count = count_in_range_cube(*sub, nanobots)

            if all(r == l+1 for l, r in zip(*sub)):
                # Volume 1 cube, no need to subdivide further
                optimal = min(optimal, (-count, sum(map(abs, sub[0]))))

            else:
                heappush(h, (-count, *sub))

if __name__=="__main__":
    nanobots = read("23_nanobots/input.txt")
    print(part1(nanobots))
    print(part2(nanobots))
