#!/usr/bin/env python3

from heapq import heappush, heappop

def geological_index(x, y, targetx, targety, depth):
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    if x == targetx and y == targety:
        return 0

    return erosion(x-1, y, targetx, targety, depth) *\
        erosion(x, y-1, targetx, targety, depth)

def erosion(x, y, targetx, targety, depth, cache={}):
    if (x, y) in cache:
        return cache[(x, y)]

    ret = (geological_index(x, y, targetx, targety, depth) + depth) % 20183
    cache[(x, y)] = ret
    return ret

def terrain(*args):
    return erosion(*args) % 3

def risk(targetx, targety, depth):
    return sum(terrain(x, y, targetx, targety, depth)
        for y in range(targety+1) for x in range(targetx + 1)
        )

CLIMBING = 0
TORCH = 1
NEITHER = 2
def passable(terrain, tool):
    if tool == CLIMBING:
        return terrain in [0, 1]
    elif tool == TORCH:
        return terrain in [0, 2]
    elif tool == NEITHER:
        return terrain in [1, 2]

def adjacent(time, x, y, tool):
    if x > 0:
        yield time+1, x-1, y, tool
    if y > 0:
        yield time+1, x, y-1, tool
    yield time+1, x+1, y, tool
    yield time+1, x, y+1, tool

    for t in range(3):
        if t != tool:
            yield time+7, x, y, t

def heuristic(time, x, y, targetx, targety):
    return time + abs(targetx - x) + abs(targety - y)

def path_finding(targetx, targety, depth):

    # heap stores tuples: (heuristic, time, x, y, tool)
    h = [(heuristic(0, 0, 0, targetx, targety), 0, 0, 0, TORCH)]
    distance = {(0, 0, TORCH): 0}
    target = (targetx, targety, TORCH)

    while h:
        t_h, time, x, y, tool = heappop(h)

        if target in distance and distance[target] <= t_h:
            return distance[target]

        if time > distance[(x, y, tool)]:
            continue

        for time, x, y, tool in adjacent(time, x, y, tool):

            if not passable(terrain(x, y, targetx, targety, depth), tool):
                continue

            if (x, y, tool) not in distance or time < distance[(x, y, tool)]:
                distance[(x, y, tool)] = time
                heappush(h,
                    (heuristic(time, x, y, targetx, targety), time, x, y, tool)
                    )

if __name__=="__main__":
    with open("22_cave/input.txt", 'r') as f:
        u = f.read().split()
        depth = int(u[1])
        targetx, targety = map(int, u[-1].split(','))

    print(risk(targetx, targety, depth))

    time = path_finding(targetx, targety, depth)
    print(time)
