#!/usr/bin/env python3

from wood import evolve, resource_value, make_str

def assertEqual(x, y):
    try:
        assert x == y
    except AssertionError:
        print("{} != {}".format(x, y))
        raise

grid = []
with open("18_lumber/test_input.txt", 'r') as f:
    for line in f:
        grid.append([c for c in line.strip()])
n = len(grid)

# workspace for evolution
grid2 = [[None]*n for _ in range(n)]

for i in range(10):
    evolve(n, grid, grid2)
    grid, grid2 = grid2, grid

print(make_str(grid))

trees, lumberyards = resource_value(grid)
assertEqual(trees, 37)
assertEqual(lumberyards, 31)
