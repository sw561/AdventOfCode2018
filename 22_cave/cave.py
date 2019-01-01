#!/usr/bin/env python3

from heapq import heappush, heappop

def geological_index(x, y, targetx, targety, depth):
    if x == 0 and y == 0:
        return 0
    if x == targetx and y == targety:
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271

    return erosion(x-1, y, targetx, targety, depth) *\
        erosion(x, y-1, targetx, targety, depth)

def cache(f):
    c = {}
    def cached(*args):
        if args not in c:
            c[args] = f(*args)
        return c[args]
    return cached

@cache
def erosion(x, y, targetx, targety, depth):
    return (geological_index(x, y, targetx, targety, depth) + depth) % 20183

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

def path_finding(targetx, targety, depth):

    # heap stores tuples: (time, x, y, tool)
    h = [(0, 0, 0, TORCH)]
    distance = {(0, 0, TORCH): 0}
    target = (targetx, targety, TORCH)

    while h:
        time, x, y, tool = heappop(h)

        if target in distance and distance[target] <= time:
            return distance[target]

        if time > distance[(x, y, tool)]:
            continue

        for time, x, y, tool in adjacent(time, x, y, tool):

            if not passable(terrain(x, y, targetx, targety, depth), tool):
                continue

            if (x, y, tool) not in distance or time < distance[(x, y, tool)]:
                distance[(x, y, tool)] = time
                heappush(h, (time, x, y, tool))

if __name__=="__main__":
    with open("22_cave/input.txt", 'r') as f:
        u = f.read().split()
        depth = int(u[1])
        targetx, targety = map(int, u[-1].split(','))

    print(risk(targetx, targety, depth))

    time = path_finding(targetx, targety, depth)
    print(time)
