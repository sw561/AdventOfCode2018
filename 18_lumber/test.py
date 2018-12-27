#!/usr/bin/env python3

from wood import main, part1

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

grid = main("18_lumber/test_input.txt")
print("\n".join("".join(c for c in line) for line in grid))

trees, lumberyards = part1(grid)
assertEqual(trees, 37)
assertEqual(lumberyards, 31)
