#!/usr/bin/env python3

from tasks import part1, process

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test1():
    for i, j in zip(part1(tasks), "CABDFE"):
        assertEqual(i, j)

with open("07_gantt/test_input.txt", 'r') as f:
    tasks = [process(line) for line in f]
test1()
