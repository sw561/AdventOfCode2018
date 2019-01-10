#!/usr/bin/env python3

from collections import deque
from itertools import count

def process(fname):
    d = dict()
    with open(fname, 'r') as f:
        for line in f:
            if line.startswith("initial state"):
                state_string = line[14:].strip()
            else:
                u = line.split()
                if u:
                    d[u[0]] = u[2]

    return d, state_string

class State:
    def __init__(self, i, d):
        # i is index corresponding to first element in d
        # d is a deque with '.' or '#' for dead and live plants
        self.i = i
        self.d = d

    def __iter__(self):
        # yield plant states with ends as required for use in evolve
        yield from self.d
        for _ in range(4):
            yield '.'

    def __str__(self):
        return "{:3d} {}".format(self.i, "".join(iter(self.d)))

    def evolve(self, translate):
        new_i = self.i - 2
        new_d = deque()

        temp = deque('.....', maxlen=5)
        for x in iter(self):
            temp.append(x)
            new_d.append(translate.get("".join(temp), '.'))

        while new_d[0] == '.':
            new_d.popleft()
            new_i += 1

        while new_d[-1] == '.':
            new_d.pop()

        return State(new_i, new_d)

    def sum(self):
        return sum(i for i, x in zip(count(start=self.i), self.d) if x == '#')

def sum_generator(state, translate):
    for i in count(start=1):
        state = state.evolve(translate)
        s = state.sum()
        # Print here to see visually what is happening
        # print(i, state, s)
        yield i, s

if __name__=="__main__":
    d, state_string = process("12_plants/input.txt")

    state = State(0, deque(state_string))
    g = sum_generator(state, d)

    # part 1
    for _ in range(20):
        x = next(g)
    print(x[1])

    # part 2
    sums = deque(maxlen=4)
    # Continue until the sums are consistenly changing linearly
    while len(sums) < 4 or not all(sums[i] == sums[0] + i*(sums[1] - sums[0]) for i in range(2, len(sums))):

        i, x = next(g)
        sums.append(x)

    final_value = sums[-1] + (sums[1] - sums[0]) * (int(5e10) - i)
    print(final_value)
