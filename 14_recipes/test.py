#!/usr/bin/env python3

from recipes import solve

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

tests = [
(   5, "0124515891"),
(   9, "5158916779"),
(  18, "9251071085"),
(2018, "5941429882"),
]

def test():
    for n, digits in tests:
        r = solve([int(x) for x in digits])
        assertEqual(len(r), n + len(digits))

test()
