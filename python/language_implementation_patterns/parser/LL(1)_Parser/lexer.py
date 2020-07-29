class Token:

    def __init__(self, type, text):
        self.type = type
        self.text = text

    def __str__(self):
        name = Lexer.token_names[self.type]
        return '<' + self.text + ',' + name + '>'


class Lexer:

    EOF = 1
    NAME = 2
    COMMA = 3
    LBRACK = 4
    RBRACK = 5    
    token_names = ['n/a', '<EOF>', 'NAME', 'COMMA', 'LBRACK', 'RBRACK']

    def __init__(self, input):
        self.input = input
        self.pointer = 0
        self.current = self.input[self.pointer]

    def get_token_name(self, x):
        return Lexer.token_names[x]

    def is_letter(self):
        return self.current.isalpha()

    def consume(self):
        self.pointer += 1
        if self.pointer >= len(self.input):
            self.current = None
        else:
            self.current = self.input[self.pointer]

    def match(self, x):
        if self.current == x:
            self.consume()
        else:
            raise Exception('excepting ' + str(x) + '; found ' + str(self.current))

    def next_token(self):
        while self.current:
            if self.current == ' ' or self.current == '\t' or self.current == '\n' or self.current == '\r':
                self.ws()
            if self.current == ',':
                self.consume()
                return Token(Lexer.COMMA, ',')
            elif self.current == '[':
                self.consume()
                return Token(Lexer.LBRACK, '[')
            elif self.current == ']':
                self.consume()
                return Token(Lexer.RBRACK, ']')
            else:
                if self.is_letter():
                    return self.name()
                raise Exception('invalide character: ' + self.current)
        return Token(Lexer.EOF, "<EOF>")

    def name(self):
        buffer = ''
        while True:
            buffer += self.current
            self.consume()
            if not self.is_letter():
                break
        return Token(Lexer.NAME, buffer)

    def ws(self):
        while self.current == ' ' or self.current == '\t' or self.current == '\n' or self.current == '\r':
            self.consume()


class Parser:

    def __init__(self, input, k):
        self.input = input
        self.lookahead = []
        self.k = k
        self.p = 0
        for i in range(0, k):
            self.consume()

    def consume(self):
        self.lookahead[p] = self.input.next_token()
        self.p = (self.p+1) % self.k


if __name__ == '__main__':
    lexer = Lexer('[a, b]')
    t = lexer.next_token()
    while t.type != Lexer.EOF:
        print(t)
        t = lexer.next_token()
