#!/usr/bin/env python3

from stars_align import process, bisection, spread, display

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

with open("10_stars/test_input.txt", 'r') as f:
    data = [process(line, pos_size=2) for line in f]

t = bisection(lambda x: spread(data, x))
# Part 1
display(data, t)

# test for part 2
assertEqual(t, 3)
