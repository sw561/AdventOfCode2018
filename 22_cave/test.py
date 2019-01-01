
from cave import erosion, risk

depth = 510
targetx, targety = 10, 10

def terrain_type(*args):
    if (args[0], args[1]) == (0, 0):
        return 'M'
    elif (args[0], args[1]) == (args[2], args[3]):
        return 'T'
    u = erosion(*args)
    return ['.', '=', '|'][u % 3]

for y in range(16):
    for x in range(16):
        print(terrain_type(x, y, targetx, targety, depth), end='')
    print()

print(risk(targetx, targety, depth))
