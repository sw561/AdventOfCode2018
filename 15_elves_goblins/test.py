#!/usr/bin/env python3

from elves import process_grid, play

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test1(fname):
    with open(fname, 'r') as f:
        inp = [line.strip() for line in f]

    grid, agents = process_grid(inp)

    round_counter, g = play(grid, agents)
    print("\nRound: {}".format(round_counter))
    g.display()
    return round_counter, g.total_hitpoints()

assertEqual(test1("15_elves_goblins/test_input2.txt"), (47, 590))
assertEqual(test1("15_elves_goblins/test_input3.txt"), (37, 982))
