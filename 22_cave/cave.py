#!/usr/bin/env python3

def geological_index(x, y, targetx, targety, depth):
    if x == 0 and y == 0:
        return 0
    if x == targetx and y == targety:
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271

    return erosion(x-1, y, targetx, targety, depth) * erosion(x, y-1, targetx, targety, depth)

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

def risk(targetx, targety, depth):
    return sum(erosion(x, y, targetx, targety, depth) % 3
        for y in range(targety+1) for x in range(targetx + 1)
        )

if __name__=="__main__":
    with open("22_cave/input.txt", 'r') as f:
        u = f.read().split()
        depth = int(u[1])
        targetx, targety = map(int, u[-1].split(','))

    print(risk(targetx, targety, depth))
