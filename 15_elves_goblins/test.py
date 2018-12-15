#!/usr/bin/env python3

from elves import part1

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

assertEqual(part1("15_elves_goblins/test_input2.txt"), (47, 590))
assertEqual(part1("15_elves_goblins/test_input3.txt", verbose=True), (37, 982))
