#!/usr/bin/env python3

from itertools import cycle

def part1(changes):
    return sum(changes)

def part2(changes):
    freq = 0
    visited = set()
    changes = cycle(changes)

    while freq not in visited:
        visited.add(freq)
        freq += next(changes)

    return freq

if __name__=="__main__":
    with open("01_frequency_changes/input.txt", 'r') as f:
        changes = [int(x) for x in f]

    print(part1(changes))
    print(part2(changes))
