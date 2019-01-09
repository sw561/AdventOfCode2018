#!/usr/bin/env python3

from infection import read_file, play_game

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test1():
    groups = read_file("24_infection/test_input.txt")

    remaining, army = play_game(groups)
    assertEqual(remaining, 5216)
    assertEqual(army, 1)

    remaining, army = play_game(groups, 1570)
    assertEqual(remaining, 51)
    assertEqual(army, 0)

test1()
