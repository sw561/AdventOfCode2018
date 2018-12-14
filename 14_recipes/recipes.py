#!/usr/bin/env python3

def part1(n):
    u = [3, 7]
    p1 = 0
    p2 = 1

    while len(u) < n + 10:

        x = u[p1] + u[p2]
        if x // 10:
            u.append(1)
        u.append(x % 10)

        p1 = (p1 + 1 + u[p1]) % len(u)
        p2 = (p2 + 1 + u[p2]) % len(u)

    return u[n:n+10]

def part2(inp):
    u = [3, 7]
    p1 = 0
    p2 = 1

    while True:
        x = u[p1] + u[p2]
        if x // 10:
            u.append(1)
            if all(x == y for x, y in zip(reversed(u), reversed(inp))):
                return u
        u.append(x % 10)
        if all(x == y for x, y in zip(reversed(u), reversed(inp))):
            return u

        p1 = (p1 + 1 + u[p1]) % len(u)
        p2 = (p2 + 1 + u[p2]) % len(u)

if __name__=="__main__":
    with open("14_recipes/input.txt", 'r') as f:
        inp = f.read().strip()

    print("".join(map(str, part1(int(inp)))))

    u = part2([int(x) for x in inp])
    print(len(u) - len(inp))
