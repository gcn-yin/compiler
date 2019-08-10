from collections import namedtuple

class Env:
    def __init__(self):
        self.env = []

    def extend_env_record(self, symbol, val):
        pair = [symbol, val]
        self.env = [pair, self.env]
        return self

    def apply(self, sym):
        return self.__apply(sym, self.env)

    def __apply(self, search_sym, env):
        if env == []:
            raise Exception("Empty Env")
        print(env)
        sym = env[0][0]
        val = env[0][1]
        old_env = env[1]
        if (search_sym == sym.var):
            print("eq!")
            return val
        return self.__apply(search_sym, old_env)

NumVal = namedtuple('NumVal', ['value'])
BoolVal = namedtuple('BoolVal', ['boolean'])

ConstExp = namedtuple('ConstExp', ['num'])
VarExp = namedtuple('VarExp', ['var'])
DiffExp = namedtuple('DiffExp', ['exp1', 'exp2'])
ZeroExp = namedtuple('ZeroExp', ['exp1'])
IfExp = namedtuple('IfExp', ['exp1', 'exp2', 'exp3'])
LetExp = namedtuple('LetExp', ['var', 'exp1', 'body'])

def value_of(exp, env):
    if isinstance(exp, ConstExp):
        return NumVal(exp.num)
    elif isinstance(exp, VarExp):
        return env.apply(exp.var)
    elif isinstance(exp, DiffExp):
        exp1 = exp.exp1
        exp2 = exp.exp2
        val1 = value_of(exp1, env)
        val2 = value_of(exp2, env)
        num1 = val1.value
        num2 = val2.value
        return NumVal(num1 - num2)
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
        return value_of(body, env.extend_env_record(var, val1))
        


'''
use pytest to test
$ pytest let_lang.py
...
'''
def test2():
    env = Env()
    exp = LetExp(
        VarExp('a'),
        ConstExp(1),
        IfExp(
            ZeroExp(VarExp('a')),
            DiffExp(VarExp('a'), ConstExp(1)),
            DiffExp(VarExp('a'), ConstExp(2))
        )
    )
    assert value_of(exp, env) == NumVal(-1)