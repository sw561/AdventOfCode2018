#!/usr/bin/env python3

import re

def positions(data, time):
    return [(px + vx*time, py + vy*time) for px, py, vx, vy in data]

def spread(data, t):
    pos = positions(data, t)

    xmin = min(p[0] for p in pos)
    xmax = max(p[0] for p in pos)
    ymin = min(p[1] for p in pos)
    ymax = max(p[1] for p in pos)

    return xmax - xmin + ymax - ymin

def eval_derivative(f, x):
    # ''' derivative '''
    # for function f which takes integers only, return 0 if derivative changes
    # sign at x, otherwise use centred differencing
    yl = f(x-1)
    y  = f(x)
    yr = f(x+1)

    if yl > y and y < yr:
        return y, 0
    else:
        return y, (yr - yl) / 2

def bisection(f):
    # Using only integer arguments, find minimum of f

    xl = 0
    yl = f(xl)
    xr = 1
    yr = f(xr)
    ml = yr - yl

    # print(xl, yl, ml, xr, yr)

    xr = int(xl - yl * (xr-xl) / (yr-yl))

    yr, mr = eval_derivative(f, xr)

    while xr - xl > 2:
        # print(xl, yl, ml, xr, yr, mr, end=' ')

        # This is intersection point of the two lines
        x = int((yr - mr*xr - yl + ml*xl) / (ml - mr))
        # print("Trying: {}".format(x))
        y, m = eval_derivative(f, x)
        if m > 0:
            xr, yr, mr = x, y, m
        elif m < 0:
            xl, yl, ml = x, y, m
        else:
            return x

    return (xr+xl) // 2

def display(data, t):
    pos = positions(data, t)

    xmin = min(p[0] for p in pos)
    xmax = max(p[0] for p in pos)
    ymin = min(p[1] for p in pos)
    ymax = max(p[1] for p in pos)

    data = [['.']*(1 + xmax - xmin) for _ in range(1 + ymax - ymin)]

    for px, py in pos:
        data[py-ymin][px-xmin] = '#'

    for row in data:
        print("".join(x for x in row))

    return data

if __name__=="__main__":
    pattern = re.compile("-?\d+")
    with open("10_stars/input.txt", 'r') as f:
        data = [tuple(map(int, re.findall(pattern, line))) for line in f]

    t = bisection(lambda x: spread(data, x))
    # part 1
    display(data, t)
    # part 2
    print(t)
