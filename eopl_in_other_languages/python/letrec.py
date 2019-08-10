from collections import namedtuple


NumVal = namedtuple('NumVal', ['value'])
BoolVal = namedtuple('BoolVal', ['boolean'])
ProcVal = namedtuple('ProcVal', ['proc'])
Procedure = namedtuple('Procedure', ['var', 'body', 'env'])

ConstExp = namedtuple('ConstExp', ['num'])
VarExp = namedtuple('VarExp', ['var'])
DiffExp = namedtuple('DiffExp', ['exp1', 'exp2'])
ZeroExp = namedtuple('ZeroExp', ['exp1'])
IfExp = namedtuple('IfExp', ['exp1', 'exp2', 'exp3'])
LetExp = namedtuple('LetExp', ['var', 'exp1', 'body'])
ProcExp = namedtuple('ProcExp', ['var', 'body'])
CallExp = namedtuple('CallExp', ['rator', 'rand'])
LetRecExp = namedtuple('LetRecExp', ['name', 'var', 'body', 'letrec_body'])

EmptyEnv = namedtuple('EmptyEnv', [])
ExtendEnv = namedtuple('ExtendEnv', ['var', 'val', 'saved_env'])
ExtendEnvRec = namedtuple('ExtendEnvRec', ['name', 'var', 'body', 'saved_env'])


def apply_env(search_sym, env):
    if isinstance(env, EmptyEnv):
        raise Exception("Empty Env")
    elif isinstance(env, ExtendEnv):
        var = env.var
        val = env.val
        saved_env = env.saved_env
        if search_sym == var:
            return val
        return apply_env(search_sym, saved_env)
    elif isinstance(env, ExtendEnvRec):
        name = env.name
        var = env.var
        body = env.body
        saved_env = env.saved_env
        if search_sym == name:
            return ProcVal(Procedure(var, body, env))
        return apply_env(search_sym, saved_env)


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
        return value_of(body, ExtendEnv(var, val1, env))
    elif isinstance(exp, ProcExp):
        var = exp.var
        body = exp.body
        return ProcVal(Procedure(var, body, env))
    elif isinstance(exp, CallExp):
        rator = exp.rator
        rand = exp.rand
        proc = value_of(rator, env).proc
        arg = value_of(rand, env)
        return apply_procedure(proc, arg)
    elif isinstance(exp, LetRecExp):
        name = exp.name
        var = exp.var
        body = exp.body
        letrec_body = exp.letrec_body
        return value_of(letrec_body, ExtendEnvRec(name, var, body, env))


def apply_procedure(proc, arg):
    if isinstance(proc, Procedure):
        var = proc.var
        body = proc.body 
        saved_env = proc.env
        return value_of(body, ExtendEnv(var, arg, saved_env))

'''
use pytest to test
$ pytest let_lang.py
...
'''


def test2():
    env = EmptyEnv()
    exp = LetRecExp(
        'double',
        'x',
        IfExp(
            ZeroExp(VarExp('x')),
            ConstExp(0),
            DiffExp(
                CallExp(
                    VarExp('double'),
                    DiffExp(
                        VarExp('x'),
                        ConstExp(1)
                    )
                ),
                ConstExp(-2)
            )
        ),
        CallExp(
            VarExp('double'),
            ConstExp(6)
        )
    )
    assert value_of(exp, env) == NumVal(12)
