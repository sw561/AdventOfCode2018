#!/usr/bin/env python3

from clever import solve

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test_f():
    changes = [+1, -2, +3, +1]
    assertEqual(solve(changes), (3, 2))

    changes = [+3, +3, +4, -2, -4]
    assertEqual(solve(changes), (4, 10))

    changes = [-x for x in changes]
    assertEqual(solve(changes), (-4, -10))

    changes = [-6, +3, +8, +5, -6]
    assertEqual(solve(changes), (4, 5))

    changes = [+7, +7, -2, -7, -4]
    assertEqual(solve(changes), (1, 14))

    changes = [+1, -1]
    assertEqual(solve(changes), (0, 0))

    changes = [3, 5, -5]
    assertEqual(solve(changes), (3, 3))

    changes = [3, 5, 1, -1, -5]
    assertEqual(solve(changes), (3, 8))

    changes = [3, 5, -5, -3]
    assertEqual(solve(changes), (0, 3))

    changes = [3, 5, -5, -3, 1]
    assertEqual(solve(changes), (1, 3))

    print("Tests passed")

test_f()
