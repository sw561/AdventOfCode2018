#!/usr/bin/env python3

from itertools import chain
from collections import defaultdict
from heapq import heappush, heappop
from copy import deepcopy

def make_dicts(tasks):
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

    return requirements, required_by, h

def part1(requirements, required_by, h):
    while h:
        n = heappop(h)
        yield n
        for c in required_by[n]:
            requirements[c].remove(n)
            if not requirements[c]:
                heappush(h, c)

def part2(requirements, required_by, h, n_workers=5, worker_time=60, verbose=False):

    workers_busy = 0

    # Heap of (time, task_completions) to be processed
    time_heap = [(0, None)]

    while time_heap:
        time, complete = heappop(time_heap)

        # Process newly completed job
        if complete is not None:
            workers_busy -= 1
            for c in required_by[complete]:
                requirements[c].remove(complete)
                if not requirements[c]:
                    heappush(h, c)
            if verbose:
                print("Time: {:4d} - Completed job {}".format(time, complete))

        # Assign new tasks
        while h and workers_busy < n_workers:
            task = heappop(h)
            workers_busy += 1
            heappush(time_heap, (time + worker_time + ord(task) - ord('A') + 1, task))

    return time

def process(line):
    s = line.split()
    return s[1], s[7]

if __name__=="__main__":
    with open("07_gantt/input.txt", 'r') as f:
        tasks = [process(line) for line in f]

    requirements, required_by, h = make_dicts(tasks)

    # Need to deepcopy so we can reuse in part2
    print("".join(part1(deepcopy(requirements), deepcopy(required_by), deepcopy(h))))

    print(part2(requirements, required_by, h))
