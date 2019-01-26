#!/usr/bin/env python3

def solve(inp):

    inp = list(reversed(inp))

    u = [3, 7]
    p1 = 0
    p2 = 1

    def check():
        for i, x in enumerate(inp):
            if x != u[-1-i]:
                return False
        return True

    while True:
        x = u[p1] + u[p2]

        if x >= 10:
            u.append(1)
            if check():
                return u
            u.append(x-10)
        else:
            u.append(x)

        if check():
            return u

        lu = len(u)
        p1 = (p1 + 1 + u[p1]) % lu
        p2 = (p2 + 1 + u[p2]) % lu

    return u

if __name__=="__main__":
    with open("14_recipes/input.txt", 'r') as f:
        inp = [int(x) for x in f.read().strip()]

    u = solve(inp)

    # Part 1
    n = int("".join(map(str, inp)))
    print("".join(map(str, u[n:n+10])))

    # Part 2
    print(len(u) - len(inp))
