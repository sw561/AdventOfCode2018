#!/usr/bin/env python3

from itertools import chain
from collections import defaultdict
from heapq import *

def part1(tasks):
    # task[i] = (a, b) means task A must be done before b

    # requirements[i] is set of tasks which must be done before i
    requirements = defaultdict(set)

    # required_by[i] is the list of tasks which can be reconsidered once i is done
    required_by = defaultdict(list)

    for a, b in tasks:
        requirements[b].add(a)
        required_by[a].append(b)

    h = []
    for task in set(chain(requirements.keys(), required_by.keys())):
        if not requirements[task]:
            heappush(h, task)

    while h:
        n = heappop(h)
        yield n
        for c in required_by[n]:
            requirements[c].remove(n)
            if not requirements[c]:
                heappush(h, c)

def process(line):
    s = line.split()
    return s[1], s[7]

if __name__=="__main__":
    with open("07_gantt/input.txt", 'r') as f:
        tasks = [process(line) for line in f]

    print("".join(part1(tasks)))
