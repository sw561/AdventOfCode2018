#!/usr/bin/env python3

import re
from stars_align import bisection, spread, display

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

pattern = re.compile("-?\d+")
with open("10_stars/test_input.txt", 'r') as f:
    data = [tuple(map(int, re.findall(pattern, line))) for line in f]

t = bisection(lambda x: spread(data, x))
# Part 1
display(data, t)

# test for part 2
assertEqual(t, 3)
