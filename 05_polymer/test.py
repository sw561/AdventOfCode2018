#!/usr/bin/env python3

from polymer import reacted, part2

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test():
    polymer = "dabAcCaCBAcCcaDA"

    r = reacted(map(ord, polymer))
    assertEqual("".join(map(chr, r)), "dabCBAcaDA")
    assertEqual(len(r), 10)
    assertEqual(part2(r), 4)

    print("Tests passed")

test()
