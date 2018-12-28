# Can be used for day 16 as well as day 19

funcs = {}

class Func:
    def __init__(self, f, name, a_reg=0, b_reg=0):
        self.f = f
        self.a_reg = a_reg
        self.b_reg = b_reg
        self.__name__ = name

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

                # Since set has to be defined with leading underscore to avoid
                # overwriting builtin set function
                if name.startswith("_"):
                    name = name[1:]

                funcs[name] = Func(f, name, a_reg, b_reg)
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
