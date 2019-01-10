#!/usr/bin/env python3

import re
from itertools import product
from heapq import heappop, heappush

def read(fname):
    nanobots = []
    pattern = re.compile("-?\d+")
    with open(fname, 'r') as f:
        for line in f:
            x = re.findall(pattern, line)
            nanobots.append(tuple(map(int, x)))

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

def multiply(g):
    p = next(g)
    for i in g:
        p *= i
    return p

def distance(left, right, x):
    if x < left:
        return left - x
    elif x >= right:
        return x - (right - 1)
    return 0

class Cube:
    def __init__(self, min_coords, max_coords):
        self.min_coords = min_coords
        self.max_coords = max_coords

    def subcubes(self):
        # Yield 8 smaller cubes

        mid = [(left + right) // 2 for left, right in zip(self.min_coords, self.max_coords)]

        for p in product(range(2), repeat=3):
            min_coords = tuple(m if pi else left for pi, left, m in\
                zip(p, self.min_coords, mid)
                )
            max_coords = tuple(right if pi else m for pi, m, right in\
                zip(p, mid, self.max_coords)
                )
            yield Cube(min_coords, max_coords)

    def in_range(self, x, y, z, r):
        d = sum(distance(l, r, u) for l, r, u in\
            zip(self.min_coords, self.max_coords, [x, y, z]))
        return d <= r

    def count_in_range(self, nanobots):
        return sum(self.in_range(*bot) for bot in nanobots)

    def size(self):
        return multiply(right - left for left, right in zip(self.min_coords, self.max_coords))

    def __str__(self):
        return "{} {}".format(self.min_coords, self.max_coords)

def part2(nanobots):
    min_coords = tuple(min(bot[i] for bot in nanobots) for i in range(3))
    max_coords = tuple(max(bot[i] for bot in nanobots) for i in range(3))

    c = Cube(min_coords, max_coords)
    count = c.count_in_range(nanobots)
    h = [(-count, c.min_coords, c)]

    optimal = None

    while h:
        mcount, _, c = heappop(h)

        if optimal is not None and mcount > optimal[0]:
            return optimal[-1]

        # print("Searching from {} {}".format(c, mcount))
        for sub in c.subcubes():
            if sub.size() == 0:
                continue

            count = sub.count_in_range(nanobots)

            if sub.size() == 1:
                d = sum(map(abs, sub.min_coords))
                o = (-count, d)
                if optimal is None or o < optimal:
                    optimal = o

            else:
                heappush(h, (-count, sub.min_coords, sub))

if __name__=="__main__":
    nanobots = read("23_nanobots/input.txt")
    print(part1(nanobots))
    print(part2(nanobots))
