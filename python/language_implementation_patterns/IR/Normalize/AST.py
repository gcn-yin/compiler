from token import Token

class Ast:

    def __init__(self, token=None):
        if type(token) == int:
            self.token = Token(token)
        else:
            self.token = token
        self.children = []

    def get_node_type(self):
        return self.token.type

    def add_child(self, t):
        self.children.append(t)

    def is_nil(self):
        return self.token == None

    def to_string_tree(self):
        if self.children == None or len(self.children) == 0:
            return str(self)
        buf = ''
        if not self.is_nil():
            buf += '('
            buf += str(self)
            buf += ' '
        for i in self.children:
            buf += ' '
            buf += str(i)
        if not self.is_nil:
            buf += ')'
        return buf

class ExprNode(Ast):
    
    tINVALID = 0
    tINTEGER = 1
    tVECTOR = 2

    def __init__(self, token=None):
        Ast.__init__(self, token)
        self.evalType = None
    
    def get_evaltype(self):
        return self.evalType
    