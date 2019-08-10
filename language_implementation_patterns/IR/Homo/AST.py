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

    def __str__(self):
        buf = ''
        if not self.is_nil():
            buf += "("
            buf += str(self.token)
            buf += ' '
        for i in self.children:
            buf += ' '
            buf += str(i)
        return buf

def main():
    plus = Token(Token.PLUS, '+')
    one = Token(Token.INT, '1')
    two = Token(Token.INT, '2')
    root = Ast(plus)
    root.add_child(Ast(one))
    root.add_child(Ast(two))
    print("1+2 tree: " + str(root))


if __name__ == '__main__':
    main()