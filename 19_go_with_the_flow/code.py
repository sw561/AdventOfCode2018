#!/usr/bin/env python3

from elfcode import funcs
from write_prog import read
from math import ceil, sqrt

def run(program):
    # Just need to know value in register[-1] when inner loop starts

    while 0 <= register[ip] < len(program):
        command, *args = program[register[ip]]
        funcs[command](register, *args)
        if register[ip] == 3:
            return register[-1]
        register[ip] += 1

def factors(x):
    for i in range(1, ceil(sqrt(x))):
        if not x%i:
            yield i
            yield x//i

    i = int(sqrt(x))
    if i**2 == x:
        yield i

if __name__=="__main__":
    ip, program = read("19_go_with_the_flow/input.txt")

    # Part 1
    register = [0]*6
    x = run(program)
    print(sum(factors(x)))

    # Part 2
    register = [0]*6
    register[0] = 1
    x = run(program)
    print(sum(factors(x)))
