# Print the program in readable format

ip = None

def read(fname):
    program = []
    with open(fname, 'r') as f:
        for line in f:
            if line.startswith('#'):
                global ip
                ip = int(line.split()[-1])
                continue

            command, *args = line.split()
            program.append([command] + [int(x) for x in args])

    return ip, program

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
            if command.startswith('b'):
                t_args[1] = "{:x}".format(args[1])
            else:
                t_args[1] = "{:2d}".format(args[1])

    t_args[2] = translate_to_reg(t_args[2])
    return t_args

def main(program):

    for i, (command, *args) in enumerate(program):
        print("{:2d}".format(i), command, end=' ')
        for x in display(command, args):
            if type(x) is str:
                print(x, end=' ')
            else:
                print("{:2d}".format(x), end=' ')

        print()

if __name__=="__main__":
    ip, program = read("19_go_with_the_flow/input.txt")
    main(program)
