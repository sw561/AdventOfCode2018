#!/usr/bin/env python3

funcs = {}

class Func:
    def __init__(self, f, a_reg=0, b_reg=0):
        self.f = f
        self.a_reg = a_reg
        self.b_reg = b_reg
        self.__name__ = f.__name__

    def __call__(self, register, a, b, c):
        if self.a_reg:
            a = register[a]
        if self.b_reg:
            b = register[b]

        register[c] = self.f(register, a, b)

def make_variants(a, b):
    def decorate(f):
        for a_reg in range(a+1):
            for b_reg in range(b+1):

                name = f.__name__
                if a:
                    name += "r" if a_reg else "i"
                if b:
                    name += "r" if b_reg else "i"

                # Dirty hack, because I only noticed we don't want these
                # functions later
                if name.endswith("ii"):
                    continue

                funcs[name] = Func(f, a_reg, b_reg)
    return decorate

@make_variants(0, 1)
def add(register, a, b):
    return register[a] + b

@make_variants(0, 1)
def mul(register, a, b):
    return register[a] * b

@make_variants(0, 1)
def ban(register, a, b):
    return register[a] & b

@make_variants(0, 1)
def bor(register, a, b):
    return register[a] | b

@make_variants(1, 0)
def _set(register, a, b):
    return a

@make_variants(1, 1)
def gt(register, a, b):
    return int(a > b)

@make_variants(1, 1)
def eq(register, a, b):
    return int(a == b)

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
