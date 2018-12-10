#!/usr/bin/env python3

from metadata import part1, part2

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

with open("08_metadata/test_input.txt", 'r') as f:
    data = [int(x) for x in f.read().split()]

assertEqual(part1(data), 138)
assertEqual(part2(data), 66)
