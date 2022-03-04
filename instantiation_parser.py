"""
Homework 2
Due Feb 21, 2022
CSCE 421
Simon Schoenbeck

This is an additional file for processing the instantiated constraints.
"""
function_names = ['neg', 'abs', 'add', 'sub', 'mul', 'div', 'mod', 'pow', 'min', 'max', 'eq',
                  'ne', 'ge', 'gt', 'le', 'lt', 'not', 'and', 'or', 'xor', 'iff', 'if']


# Integer Arithmetic:
def f_neg(args) -> int:
    a = args[0]
    return -int(a)


def f_abs(args) -> int:
    a = args[0]
    return abs(int(a))


def f_add(args) -> int:
    a, b = args[0:2]
    return int(a) + int(b)


def f_sub(args) -> int:
    a, b = args[0:2]
    return int(a) - int(b)


def f_mul(args) -> int:
    a, b = args[0:2]
    return int(a) * int(b)


def f_div(args) -> float:
    a, b = args[0:2]
    return int(a) / int(b)


def f_mod(args) -> int:
    a, b = args[0:2]
    return int(a) % int(b)


def f_pow(args) -> int:
    a, b = args[0:2]
    return int(a) ** int(b)


def f_min(args) -> int:
    a, b = args[0:2]
    return min(int(a), int(b))


def f_max(args) -> int:
    a, b = args[0:2]
    return max(int(a), int(b))


# Integer Relational:
def f_eq(args) -> bool:
    a, b = args[0:2]
    return int(a) == int(b)


def f_ne(args) -> bool:
    a, b = args[0:2]
    return int(a) != int(b)


def f_ge(args) -> bool:
    a, b = args[0:2]
    return int(a) >= int(b)


def f_gt(args) -> bool:
    a, b = args[0:2]
    return int(a) > int(b)


def f_le(args) -> bool:
    a, b = args[0:2]
    return int(a) <= int(b)


def f_lt(args) -> bool:
    a, b = args[0:2]
    return int(a) < int(b)


# Boolean Logic:
def f_not(args) -> bool:
    p = args[0]
    return not bool(p)


def f_and(args) -> bool:
    p, q = args[0:2]
    return bool(p) and bool(q)


def f_or(args) -> bool:
    p, q = args[0:2]
    return bool(p) or bool(q)


def f_xor(args) -> bool:
    p, q = args[0:2]
    return (bool(p) and not bool(q)) or (not bool(p) and bool(q))


def f_iff(args) -> bool:
    p, q = args[0:2]
    print('Encountered iff, this is implemented as logical AND')
    return bool(p) and bool(q)


# Control
def f_if(args) -> bool:
    p, a, b = args[0:3]
    if bool(p):
        return a
    return b


class CustomFunction:
    def __init__(self, name):
        self.name = name
        self.args = []
        self.execute = None
        if self.name == 'neg':
            self.execute = f_neg
        if self.name == 'abs':
            self.execute = f_abs
        if self.name == 'add':
            self.execute = f_add
        if self.name == 'sub':
            self.execute = f_sub
        if self.name == 'mul':
            self.execute = f_mul
        if self.name == 'div':
            self.execute = f_div
        if self.name == 'mod':
            self.execute = f_mod
        if self.name == 'pow':
            self.execute = f_pow
        if self.name == 'min':
            self.execute = f_min
        if self.name == 'max':
            self.execute = f_max
        if self.name == 'eq':
            self.execute = f_eq
        if self.name == 'ne':
            self.execute = f_ne
        if self.name == 'ge':
            self.execute = f_ge
        if self.name == 'gt':
            self.execute = f_gt
        if self.name == 'le':
            self.execute = f_le
        if self.name == 'lt':
            self.execute = f_lt
        if self.name == 'not':
            self.execute = f_not
        if self.name == 'and':
            self.execute = f_and
        if self.name == 'or':
            self.execute = f_or
        if self.name == 'xor':
            self.execute = f_xor
        if self.name == 'iff':
            self.execute = f_iff
        if self.name == 'if':
            self.execute = f_if

    def evaluate(self, val_dict):
        arg_names = []
        arg_eval = []
        for arg in self.args:
            if type(arg) == type(self):
                arg_names.append(arg.name)
                # print(f'This is "{self.name}" asking "{arg.name}" for eval')
                returned_val = arg.evaluate(val_dict)
                # print(f'This is "{self.name}" I got "{returned_val}" from {arg.name}')
                arg_eval.append(returned_val)
            else:
                if arg in val_dict:
                    # print(f'I have {arg} and got the value {val_dict[arg]} from val_dict')
                    arg_eval.append(val_dict[arg])
                else:
                    # Arg is not a var or function so it is assumed to be a literal
                    if arg.lower == 'False':
                        literal_val = False
                    elif arg.lower == 'True':
                        literal_val = True
                    else:
                        literal_val = int(arg)
                    # print(f'I have {arg} and got the literal {literal_val}')
                    arg_eval.append(literal_val)
        # print(self.name, arg_eval)
        return self.execute(arg_eval)
