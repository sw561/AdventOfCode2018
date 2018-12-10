#!/usr/bin/env python3

from copy import deepcopy
from tasks import process, make_dicts, part1, part2

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test1(*args):
    for i, j in zip(part1(*args), "CABDFE"):
        assertEqual(i, j)

def test2(*args, **kwargs):
    assertEqual(part2(*args, **kwargs), 15)

with open("07_gantt/test_input.txt", 'r') as f:
    tasks = [process(line) for line in f]

requirements, required_by, h = make_dicts(tasks)

test1(deepcopy(requirements), deepcopy(required_by), deepcopy(h))
test2(deepcopy(requirements), deepcopy(required_by), deepcopy(h),
    n_workers=2, worker_time=0, verbose=True
    )
