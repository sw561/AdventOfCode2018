
# Written by reading the output of write_prog.py

# First pass at ip=3
r = [0, 1, 131, 3, 1, 967]

A = 0
B = 1
C = 2
D = 3
E = 4
F = 5

while True:

    # skip r[2] commands - initial pass, skip 0
    # r[2] is either 1 or 0

    if r[B] * r[E] == r[F]:
        r[A] += r[B]

    r[E] += 1
    if r[E] > r[F]:
        r[B] += 1
        if r[B] > r[F]:
            exit()

        else:
            r[E] = 1
            print(r)
            input()
