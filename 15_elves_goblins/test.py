#!/usr/bin/env python3

from elves import process_grid, PlayCache, part2

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

def test(fname):
    with open(fname, 'r') as f:
        inp = [line.strip() for line in f]

    pc = PlayCache(*process_grid(inp))

    game = pc()
    print(game)

    elf_attack, _ = part2(pc)

    return game.round_counter, game.total_hitpoints(), elf_attack

assertEqual(test("15_elves_goblins/test_input1.txt"), (47, 590, 15))
assertEqual(test("15_elves_goblins/test_input2.txt"), (37, 982, 4))
