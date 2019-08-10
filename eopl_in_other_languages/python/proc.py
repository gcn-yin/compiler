from collections import namedtuple

# class Env:
#     def __init__(self):
#         self.env = []

#     def extend_env_record(self, symbol, val):
#         pair = [symbol, val]
#         self.env = [pair, self.env]
#         return self

#     def apply(self, sym):
#         return self.__apply(sym, self.env)

#     def __apply(self, search_sym, env):
#         if env == []:
#             raise Exception("Empty Env")
#         print(env)
#         sym = env[0][0]
#         val = env[0][1]
#         old_env = env[1]
#         if (search_sym == sym.var):
#             print("eq!")
#             return val
#         return self.__apply(search_sym, old_env)

NumVal = namedtuple('NumVal', ['value'])
BoolVal = namedtuple('BoolVal', ['boolean'])
ProcVal = namedtuple('ProcVal', ['proc'])

ConstExp = namedtuple('ConstExp', ['num'])
VarExp = namedtuple('VarExp', ['var'])
DiffExp = namedtuple('DiffExp', ['exp1', 'exp2'])
ZeroExp = namedtuple('ZeroExp', ['exp1'])
IfExp = namedtuple('IfExp', ['exp1', 'exp2', 'exp3'])
LetExp = namedtuple('LetExp', ['var', 'exp1', 'body'])
ProcExp = namedtuple('ProcExp', ['var', 'body'])
CallExp = namedtuple('CallExp', ['rator', 'rand'])


def extend_env(sym, val, old_env):
    return ((sym, val), old_env)

def apply_env(search_sym, env):
    if env == ():
        raise Exception("Empty Env")
    sym = env[0][0].var
    val = env[0][1]
    old_env = env[1]
    if (search_sym == sym):
        return val
    return apply_env(search_sym, old_env)


def value_of(exp, env):
    if isinstance(exp, ConstExp):
        return NumVal(exp.num)
    elif isinstance(exp, VarExp):
        return apply_env(exp.var, env)
    elif isinstance(exp, DiffExp):
        exp1 = exp.exp1
        exp2 = exp.exp2
        val1: NumVal = value_of(exp1, env)
        val2: NumVal = value_of(exp2, env)
        num1: int = val1.value
        num2: int = val2.value
        result = NumVal(num1 - num2)
        return result
    elif isinstance(exp, ZeroExp):
        exp1 = exp.exp1
        val1 = value_of(exp1, env)
        num1 = val1.value
        if num1 == 0:
            return BoolVal(True)
        return BoolVal(False)
    elif isinstance(exp, IfExp):
        exp1 = exp.exp1
        exp2 = exp.exp2
        exp3 = exp.exp3
        val1: bool = value_of(exp1, env).boolean
        if val1:
            return value_of(exp2, env)
        return value_of(exp3, env)
    elif isinstance(exp, LetExp):
        var = exp.var
        exp1 = exp.exp1
        body = exp.body
        val1 = value_of(exp1, env)
        return value_of(body, extend_env(var, val1, env))
    elif isinstance(exp, ProcExp):
        var = exp.var
        body = exp.body
        return ProcVal(procedure(var, body, env))
    elif isinstance(exp, CallExp):
        rator = exp.rator
        rand = exp.rand
        proc = value_of(rator, env).proc
        arg = value_of(rand, env)
        return proc(arg)
        
def procedure(var, body, env):
    def new_proc(val):
        new_env = extend_env(var, val, env)
        return value_of(body, new_env)
    return new_proc

'''
use pytest to test
$ pytest let_lang.py
...
'''
def test2():
    env = ()
    exp = LetExp(
        VarExp('x'),
        ConstExp(200),
        LetExp(
            VarExp('f'),
            ProcExp(
                VarExp('z'),
                DiffExp(VarExp('z'), VarExp('x'))
            ),
            LetExp(
                VarExp('x'),
                ConstExp(100),
                LetExp(
                    VarExp('g'),
                    ProcExp(
                        VarExp('z'),
                        DiffExp(
                            VarExp('z'),
                            VarExp('x')
                        )
                    ),
                    DiffExp(
                        CallExp(
                            VarExp('f'),
                            ConstExp(1)
                        ),
                        CallExp(
                            VarExp('g'),
                            ConstExp(1)
                        )
                    )
                )
            )
        ))
    assert value_of(exp, env) == NumVal(-100)
