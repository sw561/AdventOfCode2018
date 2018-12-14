#!/usr/bin/env python3

from recipes import part1, part2

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

def test1():
    for i, o in tests:
        assertEqual("".join(map(str, part1(i))), o)

def test2():
    for o, i in tests:
        r = part2([int(x) for x in i])
        assertEqual(len(r) - len(i), o)

test1()
test2()
