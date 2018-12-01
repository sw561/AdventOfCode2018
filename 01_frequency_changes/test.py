#!/usr/bin/env python3

from clever import solve
from frequency import part1, part2

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test_input():
    yield [+1, -2, +3, +1]

    changes = [+3, +3, +4, -2, -4]
    yield changes

    yield [-x for x in changes]

    yield [-6, +3, +8, +5, -6]

    yield [+7, +7, -2, -7, -4]

    yield [+1, -1]

    yield [3, 5, -5]

    yield [3, 5, 1, -1, -5]

    yield [3, 5, -5, -3]

    yield [3, 5, -5, -3, 1]

def test_f():
    for changes in test_input():
        assertEqual(solve(changes), (part1(changes), part2(changes)))
    print("Tests passed")

test_f()
