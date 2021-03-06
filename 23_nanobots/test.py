#!/usr/bin/env python3

from nano import read, strongest, part1, part2

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

nanobots = read("23_nanobots/test_input.txt")

assertEqual(strongest(nanobots), 0)
assertEqual(part1(nanobots), 7)

nanobots = read("23_nanobots/test_input2.txt")

assertEqual(part2(nanobots), 36)
