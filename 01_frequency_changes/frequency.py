#!/usr/bin/env python3

def gen_changes(fname, repeat=False):
    # Generator to get the changes in frequency.
    # This loops round to the start if necessary.

    changes = []
    with open(fname, 'r') as f:
        for x in f:
            changes.append(int(x))
    i = 0
    while True:
        if i == len(changes):
            if repeat:
                i = 0
            else:
                return
        yield changes[i]
        i += 1

def part1(fname):
    changes = gen_changes(fname)
    return sum(changes)

def part2(fname):
    changes = gen_changes(fname, repeat=True)

    freq = 0
    visited = set()

    while freq not in visited:
        visited.add(freq)
        freq += next(changes)

    return freq

if __name__=="__main__":
    print(part1("01_frequency_changes/input.txt"))
    print(part2("01_frequency_changes/input.txt"))
