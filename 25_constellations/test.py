#!/usr/bin/env python3

from constellations import main

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

assertEqual(main("25_constellations/test_input.txt"), 2)
assertEqual(main("25_constellations/test_input1.txt"), 4)
assertEqual(main("25_constellations/test_input2.txt"), 3)
assertEqual(main("25_constellations/test_input3.txt"), 8)
