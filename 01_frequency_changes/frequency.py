#!/usr/bin/env python3

def part1(fname):
    with open(fname, 'r') as f:
        freq = 0
        for i in f:
            freq += int(i)

    return freq

def gen_changes(fname):
    # Generator to get the changes in frequency.
    # This loops round to the start if necessary.

    changes = []
    with open(fname, 'r') as f:
        for x in f:
            changes.append(int(x))
    i = 0
    while True:
        if i == len(changes):
            i = 0
        yield changes[i]
        i += 1

def part2(fname):
    changes = gen_changes(fname)

    freq = 0
    visited = set()

    while freq not in visited:
        visited.add(freq)
        freq += next(changes)

    return freq

if __name__=="__main__":
    print(part1("01_frequency_changes/input.txt"))
    print(part2("01_frequency_changes/input.txt"))
