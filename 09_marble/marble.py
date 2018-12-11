#!/usr/bin/env python3

from collections import deque

def play(last):
    game = deque([0])

    for i in range(23, last+1, 23):
        for j in range(i-22, i):
            game.rotate(-1)
            game.append(j)
        game.rotate(7)
        yield i, game.pop()
        game.rotate(-1)

def solve(players, last):
    points = [0]*players

    for i, x in play(last):
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
