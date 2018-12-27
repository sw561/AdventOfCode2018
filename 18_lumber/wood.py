#!/usr/bin/env python3

from itertools import product

OPEN = '.'
TREES = '|'
LUMBERYARD = '#'

def atleast(g, x, n):
    # Return true if g yields x n or more times
    s = 0
    for i in g:
        if i == x:
            s += 1
            if s == n:
                return True
    return False

def adjacent(grid, i, j, n):
    for dx, dy in product([-1, 0, 1], repeat=2):
        if dx+dy or dx*dy:
            x, y = i+dx, j+dy
            if 0 <= x < n and 0 <= y < n:
                yield grid[y][x]

def evolve(n, grid, grid2):
    for j in range(n):
        for i in range(n):

            # open ground
            if grid[j][i] == OPEN:
                # at least three adjacent trees to become trees
                if atleast(adjacent(grid, i, j, n), TREES, 3):
                    grid2[j][i] = TREES
                else:
                    grid2[j][i] = OPEN

            # trees
            elif grid[j][i] == TREES:
                # at least three adjacent lumberyards to become lumberyard
                if atleast(adjacent(grid, i, j, n), LUMBERYARD, 3):
                    grid2[j][i] = LUMBERYARD
                else:
                    grid2[j][i] = TREES

            # lumberyard
            elif grid[j][i] == LUMBERYARD:
                # at least one lumberyard, one trees to remain lumberyard
                if atleast(adjacent(grid, i, j, n), TREES, 1) and\
                        atleast(adjacent(grid, i, j, n), LUMBERYARD, 1):
                    grid2[j][i] = LUMBERYARD
                else:
                    grid2[j][i] = OPEN

def part1(grid):
    trees = sum(c == TREES for line in grid for c in line)
    lumberyards = sum(c == LUMBERYARD for line in grid for c in line)
    return trees, lumberyards

def main(fname):
    grid = []
    with open(fname, 'r') as f:
        for line in f:
            grid.append([c for c in line.strip()])

    n = len(grid)

    # workspace for evolution
    grid2 = [[None]*n for _ in range(n)]

    for i in range(10):
        evolve(n, grid, grid2)
        grid, grid2 = grid2, grid

    return grid

if __name__=="__main__":
    grid = main("18_lumber/input.txt")

    trees, lumberyards = part1(grid)
    print(trees * lumberyards)
