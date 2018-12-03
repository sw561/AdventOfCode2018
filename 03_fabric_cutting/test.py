#!/usr/bin/env python3

from overlapping import overlap, process

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def grid_str(grid):
    def translate(x):
        if x is None:
            return '.'
        elif x == -1:
            return 'X'
        else:
            return str(x+1)

    return "\n".join("".join(translate(x) for x in row) for row in grid)

claims = ("#1 @ 1,3: 4x4\n"
         "#2 @ 3,1: 4x4\n"
         "#3 @ 5,5: 2x2").split("\n")
def test_process():
    expected = ("........\n"
                "...2222.\n"
                "...2222.\n"
                ".11XX22.\n"
                ".11XX22.\n"
                ".111133.\n"
                ".111133.\n"
                "........")

    grid, overlapping_claim = process(claims, size=8)
    gs = grid_str(grid)
    print(gs)
    assertEqual(gs, expected)

def test_overlap():
    part1, part2 = overlap(claims)
    assertEqual(part1, 4)
    assertEqual(part2, 3)

test_process()
test_overlap()
