#!/usr/bin/env python3

from power import power, construct_grid, power_square, find, part2

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test1():
    tests = [
    ( 8,   3,  5,  4),
    (57, 122, 79, -5),
    (39, 217,196,  0),
    (71, 101,153,  4),
    ]

    for data, x, y, p in tests:
        assertEqual(power(data, x, y), p)

def power_square_brute(data, s, x, y):
    return sum(power(data, xi, yi) for xi in range(x, x+s) for yi in range(y, y+s))

def test2():
    s = 3
    tests = [
    (18, 33, 45, 29),
    (42, 21, 61, 30),
    ]

    for data, x, y, p in tests:
        grid = construct_grid(data)
        assertEqual(power_square(grid, s, x, y), power_square_brute(data, s, x, y))
        assertEqual(power_square(grid, s, x, y), p)
        assertEqual(find(grid, s), (p, x, y))

def test3():
    tests = [
    (18, 113,  90, 269, 16),
    (42, 119, 232, 251, 12),
    ]

    for data, p, x, y, s in tests:
        grid = construct_grid(data)
        assertEqual(part2(grid), (p, x, y, s))

test1()
test2()
test3()
