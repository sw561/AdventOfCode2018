#!/usr/bin/env python3

from marble import process, solve, Circular_List

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test1():
    with open("09_marble/test_input.txt", 'r') as f:
        inp = [process(line) for line in f]

    with open("09_marble/test_output.txt", 'r') as f:
        out = [int(line) for line in f]

    for i, o in zip(inp, out):
        assertEqual(solve(*i), o)

test1()
