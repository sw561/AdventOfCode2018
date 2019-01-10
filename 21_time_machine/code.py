#!/usr/bin/env python3

from elfcode import funcs
import write_prog

def run(program):
    # Just need to know value in register[1] when it is compared to register[0]
    # they must be equal for the program to halt
    # verbose = False

    while 0 <= register[ip] < len(program):
        command, *args = program[register[ip]]
        condition = False # not (register[ip] in range(18, 26))
        if condition:
            print(register[ip], command, end=' ')
            for x in write_prog.display(command, args):
                if type(x) is str:
                    print(x, end=' ')
                else:
                    print("{:2d}".format(x), end=' ')
        funcs[command](register, *args)
        register[ip] += 1
        if condition:
            print(register)
            # x = input()
            # if x == "verbose":
            #     verbose = True
        if register[ip] == 28:
            yield register[1]

def optimized():
    b = 0

    # 6
    e = b | 65536
    b = 16298264
    while True:

        # 8
        f = e & 0xff
        b += f
        b &= 16777215
        b *= 65899
        b &= 16777215

        # print("At 13", b, e)

        if 256 > e:
            yield b

            # go to 6, manually repeat commands
            e = b | 65536
            b = 16298264
            # go to 8

        else:
            # f = 0
            # while True:
            #     d = f + 1
            #     d *= 256
            #     if d > e:
            #         # go to 26
            #         break
            #     f += 1

            # SUPER FAST OPTIMIZATION
            f = e // 256

            e = f
            # go to 8

if __name__=="__main__":
    ip, program = write_prog.read("21_time_machine/input.txt")
    # write_prog.main(program)

    register = [0]*6

    seen = set()
    first = None
    last = None
    for val in optimized(): # run(program):
        # For part 1
        # print(val)
        if first is None:
            first = val

        if val not in seen:
            seen.add(val)
            # For part 2
            last = val
        else:
            break

    print(first)
    print(last)
