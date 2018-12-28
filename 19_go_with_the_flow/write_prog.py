from code import read

# Print the program in readable format

ip, program = read("19_go_with_the_flow/input.txt")

def translate_to_reg(x):
    if x == ip:
        return "PP"
    return ' '+chr(x + ord('a'))

def display(command, args):
    t_args = args.copy()

    if command.startswith("set"):
        if command.endswith('r'):
            t_args[0] = translate_to_reg(t_args[0])
        else:
            t_args[0] = "{:2d}".format(args[0])

        t_args[1] = '  '

    else:
        if command.startswith("gt") or command.startswith("eq"):
            if command[-2] == 'r':
                t_args[0] = translate_to_reg(t_args[0])
            else:
                t_args[0] = "{:2d}".format(args[0])

        else:
            t_args[0] = translate_to_reg(t_args[0])

        if command.endswith('r'):
            t_args[1] = translate_to_reg(t_args[1])
        else:
            t_args[1] = "{:2d}".format(args[1])

    t_args[2] = translate_to_reg(t_args[2])
    return t_args

for i, (command, *args) in enumerate(program):
    print("{:2d}".format(i), command, end=' ')
    for x in display(command, args):
        if type(x) is str:
            print(x, end=' ')
        else:
            print("{:2d}".format(x), end=' ')

    print()
