#!/usr/bin/env python3

def power(data, x, y):
    rackID = x + 10
    p = (rackID * y + data) * rackID
    p = (p % 1000) // 100 - 5
    return p

def construct_grid(data):
    # each entry in grid is sum of cells above and to the left
    #
    # Can thus find total power within a square using just four entries.

    # Top row and left hand column are zero, for easy algorithm design
    grid = [[0]*301 for _ in range(301)]

    for j in range(1, 300):
        for i in range(1, 300):
            grid[j][i] = grid[j-1][i] + grid[j][i-1] - grid[j-1][i-1] + power(data, i, j)

    return grid

def power_square(grid, s, x, y):

    # bottom right corner
    xr, yr = x + s - 1, y + s - 1

    return grid[yr][xr] - grid[yr][x-1] - grid[y-1][xr] + grid[y-1][x-1]

def find(grid, s):
    # Find square of side s with largest total power, return coords of top left corner

    return max((power_square(grid, s, x, y), x, y) for x in range(300-s) for y in range(300-s))

def part1(grid):
    return find(grid, 3)

def part2(grid):
    return max((*find(grid, s), s) for s in range(300))

if __name__=="__main__":
    with open("11_fuel_cell/input.txt", 'r') as f:
        data = int(f.read())

    grid = construct_grid(data)

    ret = part1(grid)
    print(",".join(map(str, ret[1:])))

    ret = part2(grid)
    print(",".join(map(str, ret[1:])))
