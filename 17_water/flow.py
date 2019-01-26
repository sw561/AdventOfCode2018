#!/usr/bin/env python3

import re
from collections import deque

class Clay:
    def __init__(self, a, b, c, vertical=True):
        if vertical:
            self.xmin = a
            self.xmax = a
            self.ymin = b
            self.ymax = c

        else:
            self.ymin = a
            self.ymax = a
            self.xmin = b
            self.xmax = c

    def __iter__(self):
        for x in range(self.xmin, self.xmax+1):
            for y in range(self.ymin, self.ymax+1):
                yield x, y

class Grid:
    def __init__(self, clays):
        self.xmin = min(clay.xmin for clay in clays) - 1
        self.xmax = max(clay.xmin for clay in clays) + 1
        self.ymax = max(clay.ymax for clay in clays)
        self.ymin = min(clay.ymin for clay in clays)

        self.grid = [['.'] * (self.xmax - self.xmin + 1) for _ in range(self.ymax + 1)]

        for clay in clays:
            for x, y in clay:
                self.set(x, y, '#')

    def get(self, x, y):
        return self.grid[y][x - self.xmin]

    def set(self, x, y, val):
        self.grid[y][x - self.xmin] = val

    def count_water(self):
        reachable, standing = 0, 0
        for row in self.grid[self.ymin:]:
            for char in row:
                if char == '|':
                    reachable += 1
                elif char == '~':
                    standing += 1
        return reachable, standing

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid) + "\n--------------------------"

def flood_fill(grid, x, y):

    # print("Calling flood_fill with x, y = {}, {}".format(x, y))

    # Go down as far as possible
    while grid.get(x, y+1) != '#':
        grid.set(x, y, '|')
        y += 1
        if y == grid.ymax:
            grid.set(x, y, '|')
            return []

    overflow = []
    done = False

    while True:

        # Expand horizontally from x, y
        # print("Horizontal expansion from x, y = {}, {}".format(x, y))
        grid.set(x, y, '|')
        xmin = x
        xmax = x

        for inc_f in [lambda x: x-1, lambda x: x+1]:
            xi = inc_f(x)
            while grid.get(xi, y) != '#' and grid.get(xi, y+1) in ['#', '~']:
                grid.set(xi, y, '|')
                xmin = min(xmin, xi)
                xmax = max(xmax, xi)
                xi = inc_f(xi)

            if grid.get(xi, y) == '.' and grid.get(xi, y+1) == '.':
                grid.set(xi, y, '|')
                overflow.append((xi, y))
                done = True

            elif grid.get(xi, y) == '|':
                done = True

        if done:
            return overflow

        # No outflow, set the squares to ~
        for xi in range(xmin, xmax+1):
            grid.set(xi, y, '~')

        # No outflow, go up one square
        y -= 1

def read_clay(line, pattern=re.compile("\d+")):
    match = re.findall(pattern, line)
    return Clay(*map(int, match), vertical=line.startswith('x'))

def main(fname, verbose=False):
    with open(fname, 'r') as f:
        clays = [read_clay(line) for line in f]

    grid = Grid(clays)

    d = deque([(500, 1)])
    while d:
        d += flood_fill(grid, *d.popleft())

    if verbose:
        print(grid)

    # For visualisation
    # with open("o", 'w') as g:
    #     g.write(str(grid))

    reachable, standing = grid.count_water()
    # Part 1 and part 2
    return reachable + standing, standing

if __name__=="__main__":
    for x in main("17_water/input.txt"):
        print(x)
