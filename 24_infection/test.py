#!/usr/bin/env python3

from infection import read_file, Game, play_game

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test1():
    groups = read_file("24_infection/test_input.txt")

    g = Game(groups)
    remaining = play_game(g)

    assertEqual(remaining, 5216)

test1()
