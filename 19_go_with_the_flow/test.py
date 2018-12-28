#!/usr/bin/env python3

from code import read, funcs

ip, program = read("19_go_with_the_flow/test_input.txt")

register = [0]*6
while 0 <= register[ip] < len(program):
    command, *args = program[register[ip]]
    print("ip={} {} {} {}".format(
        register[ip], register, command, " ".join(map(str, args))),
        end=' ')
    funcs[command](register, *args)
    print(register)
    register[ip] += 1
