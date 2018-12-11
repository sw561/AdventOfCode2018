#!/usr/bin/env python3

# Indices used for node objects
#
# X = 0
# N = 1
# P = 2

def one_round(head, end):
    head = head[1]
    for i in range(end-22, end-1):
        after = head[1]
        new = [i, after, head]
        after[2] = new
        head[1] = new
        head = after
    i = end-1
    after = head[1]
    new = [i, after, head]
    after[2] = new
    head[1] = new

    for i in range(6):
        head = head[2]

    # Remove head and return the data corresponding to head
    data, after, before = head
    before[1] = after
    after[2] = before
    return after, data

def solve(players, last):
    head = [0, None, None]
    head[1] = head
    head[2] = head
    points = [0]*players

    for i in range(23, last+1, 23):
        head, x = one_round(head, i)
        points[i % players] += i + x

    return max(points)

def process(line):
    u = line.split()
    return int(u[0]), int(u[-2])

if __name__=="__main__":
    with open("09_marble/input.txt", 'r') as f:
       players, last  = process(f.read())

    # Part 1
    print(solve(players, last))

    # Part 2
    print(solve(players, last*100))
