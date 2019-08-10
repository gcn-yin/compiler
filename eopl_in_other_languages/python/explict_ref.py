from collections import namedtuple


NumVal = namedtuple('NumVal', ['value'])
# class NumVal:
#     def __init__(self, value):
#         self.value = value
BoolVal = namedtuple('BoolVal', ['boolean'])
ProcVal = namedtuple('ProcVal', ['proc'])
RefVal = namedtuple('RefVal', ['ref'])

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
NewRefExp = namedtuple('NewRefExp', ['exp1'])
DeRefExp = namedtuple('DeRefExp', ['exp1'])
SetRefExp = namedtuple('SetRefExp', ['exp1', 'exp2'])
class BeginExp:
    def __init__(self, exp1, *exps):
        self.exp1 = exp1
        self.exps = exps


EmptyEnv = namedtuple('EmptyEnv', [])
ExtendEnv = namedtuple('ExtendEnv', ['var', 'val', 'saved_env'])
ExtendEnvRec = namedtuple('ExtendEnvRec', ['name', 'var', 'body', 'saved_env'])


the_store: list = []
empty_store = []

def initialize_store():
    global the_store
    the_store = empty_store

def is_reference(v):
    return isinstance(v, int)

def newref(val) -> int:
    global the_store
    next_ref = len(the_store)
    the_store.append(val)
    return next_ref

def deref(ref):
    return the_store[ref]

def setref(ref, val):
    # def setref_inner(store1, ref1):
    #     if store1 == None or store1 == []:
    #         raise Exception("invalid ref")
    #     elif ref1 == 0:
    #         return [val, store1[1:-1]]
    #     else:
    #         return [store1[0], setref_inner(store1[1:-1], ref1-1)]
    # global the_store
    # return setref_inner(the_store, ref)
    global the_store
    the_store[ref] = val
    return val

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
    elif isinstance(exp, BeginExp):
        exp1 = exp.exp1
        exps = exp.exps
        def value_of_begins(e1, es):
            v1 = value_of(e1, env)
            if es == None or len(es) == 0:
                return v1
            return value_of_begins(es[0], es[1:-1])
        return value_of_begins(exp1, exps)
    elif isinstance(exp, NewRefExp):
        exp1 = exp.exp1
        v1 = value_of(exp1, env)
        result = RefVal(newref(v1))
        return result
    elif isinstance(exp, DeRefExp):
        exp1 = exp.exp1
        v1: RefVal = value_of(exp1, env)
        ref1 = v1.ref
        return deref(ref1)
    elif isinstance(exp, SetRefExp):
        exp1 = exp.exp1
        exp2 = exp.exp2
        ref = value_of(exp1, env).ref
        v2 = value_of(exp2, env)
        setref(ref, v2)
        print(the_store)
        return NumVal(23)


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
def test():
    program = LetExp(
        'g',
        LetExp(
            'counter',
            NewRefExp(ConstExp(0)),
            ProcExp(
                'dummpy',
                BeginExp(
                    SetRefExp(
                        VarExp('counter'),
                        DiffExp(
                            DeRefExp(VarExp('counter')),
                            ConstExp(-1)
                        )
                    ),
                    DeRefExp(VarExp('counter'))
                )
            )
        ),
        LetExp(
            'a',
            CallExp(
                VarExp('g'),
                ConstExp('1')
            ),
            LetExp(
                'b',
                CallExp(VarExp('g'), ConstExp(1)),
                DiffExp(VarExp('a'), VarExp('b'))
            )
        )
    )
    env = EmptyEnv()
    assert value_of(program, env) == NumVal(-1)