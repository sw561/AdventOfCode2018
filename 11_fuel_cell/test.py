#!/usr/bin/env python3

from power import power, part1

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test1():
    tests = [
    (  3,  5,  8,  4),
    (122, 79, 57, -5),
    (217,196, 39,  0),
    (101,153, 71,  4),
    ]

    for x, y, data, o in tests:
        assertEqual(power(data, x, y), o)

def test2():
    assertEqual(part1(18), (29, 33, 45))
    assertEqual(part1(42), (30, 21, 61))

test1()
test2()
