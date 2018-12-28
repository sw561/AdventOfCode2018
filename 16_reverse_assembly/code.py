#!/usr/bin/env python3

from elfcode import funcs

def find_matching_commands(before, command, after):
    for key in funcs.keys():
        register = before.copy()
        funcs[key](register, *command[1:])
        if all(r == a for r, a in zip(register, after)):
            yield key

def get_examples(fname):
    with open(fname, 'r') as f:
        inp = [line.strip() for line in f]

    i = 0
    while i < len(inp):
        line = inp[i]
        before = eval(line[line.index('['):])
        command = [int(x) for x in inp[i+1].split()]
        after = eval(inp[i+2][inp[i+2].index('['):])
        yield before, command, after
        i += 4

def part1():
    count = 0

    possible_commands = {i: set(funcs.keys()) for i in range(len(funcs))}
    possible_op_codes = {key: set(range(len(funcs))) for key in funcs.keys()}

    for args in get_examples("16_reverse_assembly/input.txt"):
        u = set(find_matching_commands(*args))
        # For part 1
        if len(u) >= 3:
            count += 1

        op_code = args[1][0]

        possible_commands[op_code] &= u

        for f in funcs.keys():
            if f not in u:
                possible_op_codes[f].discard(op_code)

    return count, possible_commands, possible_op_codes

def fix(ops, i, command, possible_commands, possible_op_codes):
    ops[i] = funcs[command]

    del possible_op_codes[command]
    del possible_commands[i]

    for c in possible_op_codes.keys():
        possible_op_codes[c].discard(i)
    for j in possible_commands.keys():
        possible_commands[j].discard(command)

def simplify(possible_commands, possible_op_codes):
    ops = [None] * 16

    change = True
    while change:
        change = False
        for i, x in possible_commands.items():
            if len(x) == 1:
                command = next(iter(x))

                change = True
                fix(ops, i, command, possible_commands, possible_op_codes)
                break

        for command, x in possible_op_codes.items():
            if len(x) == 1:
                i = next(iter(x))

                change = True
                fix(ops, i, command, possible_commands, possible_op_codes)
                break

    return ops

def part2(ops):
    register = [0,0,0,0]

    with open("16_reverse_assembly/input_part2.txt", 'r') as f:
        for line in f:
            i, *args = [int(x) for x in line.split()]
            ops[i](register, *args)

    return register

if __name__=="__main__":
    count, possible_commands, possible_op_codes = part1()
    print(count)

    ops = simplify(possible_commands, possible_op_codes)

    # for i, x in enumerate(ops):
    #     print(i, x.__name__)

    register = part2(ops)
    print(register[0])
