#!/usr/bin/env python3

from flow import main

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

x = main("17_water/test_input.txt", verbose=True)
assertEqual(x[0], 57)
assertEqual(x[1], 29)
