#!/usr/bin/env python3

import re

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

if __name__=="__main__":

    nanobots = read("23_nanobots/input.txt")

    print(part1(nanobots))
