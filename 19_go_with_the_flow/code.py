#!/usr/bin/env python3

from elfcode import funcs

register = [0]*6
ip = 0

def pointer():
    return register[ip]

def run(program, verbose=False):
    while 0 <= register[ip] < len(program):
        command, *args = program[register[ip]]
        if verbose:
            print("ip={} {} {} {}".format(
                register[ip], register, command, " ".join(map(str, args))),
                end=' ')
        funcs[command](register, *args)
        if verbose:
            print(register)
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

    return program

if __name__=="__main__":
    program = read("19_go_with_the_flow/input.txt")

    run(program)
