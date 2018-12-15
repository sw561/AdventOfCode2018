#!/usr/bin/env python3

from elves import process_grid, play, n_elf_survivors, bisection

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test(fname):
    with open(fname, 'r') as f:
        inp = [line.strip() for line in f]

    grid, agents = process_grid(inp)

    round_counter, game = play(grid, agents)
    print("\nRound: {}".format(round_counter))
    print(game)

    n_elves = sum(agent.t == 'E' for agent in agents)

    elf_attack = bisection(
        lambda x: n_elf_survivors(grid, agents, x) == n_elves, 3, 50
        )

    return round_counter, game.total_hitpoints(), elf_attack

assertEqual(test("15_elves_goblins/test_input1.txt"), (47, 590, 15))
assertEqual(test("15_elves_goblins/test_input2.txt"), (37, 982, 4))
