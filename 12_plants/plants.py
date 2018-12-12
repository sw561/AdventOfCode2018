#!/usr/bin/env python3

from itertools import chain

def process(fname):
    d = dict()
    with open(fname, 'r') as f:
        for line in f:
            if line.startswith("initial state"):
                state_string = [x for x in line[14:].strip()]
            else:
                u = line.split()
                if u:
                    d[u[0]] = u[2]

    return d, state_string

class State:
    def __init__(self, l, r):
        self.ls = ['.']*l
        self.rs = ['.']*r

    def initialise(self, state_string):
        # Use state in form of string
        for i, x in enumerate(state_string):
            self.rs[i] = x

    def copy(self):
        # Only copy sizes of arrays
        return State(len(self.ls), len(self.rs))

    def __str__(self):
        return "".join(x for x in chain(reversed(self.ls), self.rs))

    def helper(self, i):
        if i < 0:
            index = -i-1
            x = self.ls
        else:
            index = i
            x = self.rs
        return index, x

    def __getitem__(self, i):
        index, x = self.helper(i)
        if index >= len(x):
            return '.'
        else:
            return x[index]

    def __setitem__(self, i, val):
        index, x = self.helper(i)
        while index >= len(x):
            if val == '.':
                return
            x.append('.')
        x[index] = val

    def evolve(self, d):
        new = self.copy()
        for i in range(-len(self.ls)-2, len(self.rs)+2):
            new[i] = d.get("".join(self[j] for j in range(i-2, i+3)), '.')
        return new

    def sum(self):
        return sum(i for i in range(-len(self.ls), len(self.rs)) if self[i]=='#')

if __name__=="__main__":
    d, state_string = process("12_plants/input.txt")

    # Part 1
    state = State(0, len(state_string))
    state.initialise(state_string)

    for _ in range(20):
        state = state.evolve(d)
    print(state.sum())
