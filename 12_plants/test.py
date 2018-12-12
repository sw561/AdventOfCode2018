#!/usr/bin/env python3

from plants import process, State

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

if __name__=="__main__":
    d, state_string = process("12_plants/test_input.txt")

    state = State(0, len(state_string))
    state.initialise(state_string)
    print(" 0: {}".format(state))

    with open("12_plants/test_output.txt", 'r') as f:
        u = [x.strip() for x in f]

    for i, output in zip(range(20), u[1:]):
        state = state.evolve(d)
        print("{:2d}: {}".format(i+1, state))

        c = str(state)
        assert output[output.index('#'):].startswith(c[c.index('#'):])

    assertEqual(state.sum(), 325)
