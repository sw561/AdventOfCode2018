#!/usr/bin/env python3

def power(data, x, y):
    rackID = x + 10
    p = (rackID * y + data) * rackID
    p = (p % 1000) // 100 - 5
    return p

def find(data):
    # Find 3x3 square within 300x300 grid with largest total power

    for i in range(297):
        for j in range(297):
            p = sum(power(data, i+ki, j+kj) for ki in range(3) for kj in range(3))
            yield p, i, j

def part1(data):
    return max(find(data))

if __name__=="__main__":
    with open("11_fuel_cell/input.txt", 'r') as f:
        data = int(f.read())

    ret = part1(data)
    print(",".join(map(str, ret[1:])))
