#!/usr/bin/env python3

from elfcode import funcs

def run(program):
    # Just need to know value in register[-1] when inner loop starts

    while 0 <= register[ip] < len(program):
        command, *args = program[register[ip]]
        funcs[command](register, *args)
        if register[ip] == 3:
            return register[-1]
        register[ip] += 1

def read(fname):
    program = []
    with open(fname, 'r') as f:
        for line in f:
            if line.startswith('#'):
                ip = int(line.split()[-1])
                continue

            command, *args = line.split()
            program.append([command] + [int(x) for x in args])

    return ip, program

def factors(x):
    for i in range(1, x//2 + 1):
        if not x%i:
            yield i
    yield x

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
