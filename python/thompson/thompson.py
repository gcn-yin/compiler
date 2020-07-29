class FaRule:
    def __init__(self, start, content, end=[]):
        self.start: FaState = start
        self.content: list = content
        self.end: list = end 


class FaState:
    pass

def connect(first: FaRule, second: FaRule) -> tuple:
    middle = FaRule(first.end, '', second.start)
    first.end = middle
    second.start = middle
    return first, middle, second


# test
def test_connect():
    a = FaRule(FaState(), 'a', FaState())
    b = FaRule(FaState(), 'b', FaState())
    new_a, middle, new_b = connect(a, b)
    assert new_a == a
    assert new_b == b
    assert middle.content == ''

def or(first: FaRule, second: FaRule):
    head: FaState = FaState()
    tail: FaState = FaState()
    a = FaRule(head, '', first.head)
    b = FaRule(head, '', second.head)
    c = FaRule(first.end, '', tail)
    d = FaRule(second.end, '', tail)
    return a, b, c, d

def closure(rule: FaRule):
    a = FaRule(rule.end, '', rule.head)
    b = FaState()
    c = FaState()
    d = FaRule(b, '', rule.head)
    e = FaRule(b, '', c) 
    f = FaRule(rule.end, '', c)
    return d, e, f
