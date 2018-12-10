#!/usr/bin/env python3

from string import ascii_uppercase
from chronal import part1, manhattan_distance, get_total_distances

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def assertIn(x, s):
    try:
        assert x in s
    except AssertionError:
        print("{} not in {}".format(x, s))
        raise

def test1():
    m = max(map(max, points)) + 1
    DATA = [['.']*m for _ in range(m)]
    for p, letter in zip(points, ascii_uppercase):
        DATA[p[1]][p[0]] = letter

    assertEqual(part1(points, DATA), 17)

    s = "\n".join("".join(row) for row in DATA)
    print(s)

    for si, ti in zip(s, test_output):
        if ti.islower():
            assertIn(si, ['.', ti])
        elif ti.isupper():
            assertEqual(si, ti)

def brute(location, points):
    return sum(manhattan_distance(location, p) for p in points)

def test2():
    count = 0
    for location, total_distance in get_total_distances(points, threshold=32):
        count += 1
        assertEqual(total_distance, brute(location, points))

    assertEqual(count, 16)

with open("06_voronoi/test_input.txt", 'r') as f:
    points = [[int(x) for x in line.split(',')] for line in f]
with open("06_voronoi/test_output.txt", 'r') as f:
    test_output = f.read()
test1()
test2()
