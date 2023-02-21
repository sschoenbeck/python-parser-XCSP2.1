"""
Homework 2
Due Feb 21, 2022
CSCE 421
Simon Schoenbeck

This is an additional file for processing the intension constraints.
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
    """CustomFuction objects are used to enable the evaluation of intension constraints."""
    def __init__(self, name):
        self.name = name
        self.args = []
        self.execute = None
        if self.name == 'neg':
            self.execute = f_neg
        elif self.name == 'abs':
            self.execute = f_abs
        elif self.name == 'add':
            self.execute = f_add
        elif self.name == 'sub':
            self.execute = f_sub
        elif self.name == 'mul':
            self.execute = f_mul
        elif self.name == 'div':
            self.execute = f_div
        elif self.name == 'mod':
            self.execute = f_mod
        elif self.name == 'pow':
            self.execute = f_pow
        elif self.name == 'min':
            self.execute = f_min
        elif self.name == 'max':
            self.execute = f_max
        elif self.name == 'eq':
            self.execute = f_eq
        elif self.name == 'ne':
            self.execute = f_ne
        elif self.name == 'ge':
            self.execute = f_ge
        elif self.name == 'gt':
            self.execute = f_gt
        elif self.name == 'le':
            self.execute = f_le
        elif self.name == 'lt':
            self.execute = f_lt
        elif self.name == 'not':
            self.execute = f_not
        elif self.name == 'and':
            self.execute = f_and
        elif self.name == 'or':
            self.execute = f_or
        elif self.name == 'xor':
            self.execute = f_xor
        elif self.name == 'iff':
            self.execute = f_iff
        elif self.name == 'if':
            self.execute = f_if

    def evaluate(self, val_dict):
        """This function recursively computes the value of itself by paring the
         CustomFunction's arguments with the arguments in the val_dict and passing the val_dict 
         to nested functions."""
        arg_names = []
        arg_eval = []
        for arg in self.args:
            if type(arg) == type(self):
                arg_names.append(arg.name)
                returned_val = arg.evaluate(val_dict)
                arg_eval.append(returned_val)
            else:
                if arg in val_dict:
                    arg_eval.append(val_dict[arg])
                else:
                    # Arg is not a var or function so it is assumed to be a literal
                    if arg.lower == 'False':
                        literal_val = False
                    elif arg.lower == 'True':
                        literal_val = True
                    else:
                        literal_val = int(arg)
                    arg_eval.append(literal_val)
        return self.execute(arg_eval)
