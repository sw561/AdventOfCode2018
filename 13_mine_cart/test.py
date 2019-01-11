#!/usr/bin/env python3

from mine import process, play

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test1():
    with open("13_mine_cart/test_input.txt", 'r') as f:
        track = [[x for x in line if x!="\n"] for line in f]

    first_crash = play(*process(track), part1_only=True)
    assertEqual(first_crash, (3, 7))

def test2():
    with open("13_mine_cart/test_input2.txt", 'r') as f:
        track = [[x for x in line if x!="\n"] for line in f]

    _, carts = play(*process(track))
    assertEqual(carts[0][0], (4, 6))

test1()
test2()
