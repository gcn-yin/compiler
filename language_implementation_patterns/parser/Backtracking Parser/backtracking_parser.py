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
    EQUALS = 6
    token_names = ['n/a', '<EOF>', 'NAME', 'COMMA', 'LBRACK', 'RBRACK', 'EQUALS']

    def __init__(self, input):
        self.input = input
        self.pointer = 0
        self.current = self.input[self.pointer]

    def get_token_name(self, x):
        return Lexer.token_names[x]

    def is_letter(self):
        return self.current.isalpha()

    def LETTER(self):
        if self.is_letter():
            self.consume()
        else:
            raise Exception("expecting LETTER; found " + self.current)

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
            elif self.current == '=':
                self.consume()
                return Token(Lexer.EQUALS, '=')
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
    
    def __init__(self, input):
        self.input = input
        self.markers = []
        self.lookahead = []
        self.point = 0
        self.sync(1)

    def consume(self):
        self.point += 1
        if len(self.lookahead) == self.point and (not self.is_speculating()):
            self.point = 0
            self.lookahead.clear()
        
    def sync(self, i):
        if (self.point + i -1) > (len(self.lookahead) - 1):
            n = (self.point + i - 1) - (len(self.lookahead) - 1)
            self.fill(n)

    def fill(self, n):
        for i in range(0, n):
            self.lookahead.append(self.input.next_token())

    def LT(self, i):
        self.sync(i)
        return self.lookahead[self.point + i - 1]

    def LA(self, i):
        return self.LT(i).type
    
    def match(self, x):
        print(self.input.get_token_name(x))
        if self.LA(1) == x:
            self.consume()
        else:
            raise Exception("excepting " + self.input.get_token_name(x) + " found" + str(self.LT(1)))

    def mark(self):
        self.markers.append(self.point)
        return self.point

    def seek(self, index):
        self.point = index

    def release(self):
        marker = self.markers.pop()
        self.seek(marker)

    def is_speculating(self):
        return len(self.markers) > 0

    def stat(self):
        if self.speculate_stat_alt1():
            self.list()
            self.match(Lexer.EOF)
        elif self.speculate_stat_alt2():
            self.assign()
            self.match(Lexer.EOF)
        else:
            raise Exception("expecting stat found " + str(self.LT(1)))

    def speculate_stat_alt1(self):
        success = True
        self.mark()
        try:
            self.list()
            self.match(Lexer.EOF)
        except BaseException as e:
            success = False
        self.release()
        return success

    def speculate_stat_alt2(self):
        success = True
        self.mark()
        try:
            self.assign()
            self.match(Lexer.EOF)
        except BaseException as e:
            success = False
        self.release()
        return success

    def assign(self):
        self.list()
        self.match(Lexer.EQUALS)
        self.list()

    def list(self):
        self.match(Lexer.LBRACK)
        self.elements()
        self.match(Lexer.RBRACK)

    def elements(self):
        self.element()
        while self.LA(1) == Lexer.COMMA:
            self.match(Lexer.COMMA)
            self.element()

    def element(self):
        if self.LA(1) == Lexer.NAME and self.LA(2) == Lexer.EQUALS:
            self.match(Lexer.NAME)
            self.match(Lexer.EQUALS)
            self.match(Lexer.NAME)
        elif self.LA(1) == Lexer.NAME:
            self.match(Lexer.NAME)
        elif self.LA(1) == Lexer.LBRACK:
            self.list()
        else:
            raise Exception("expecting element found " + self.LT(1))

def main():
    lexer = Lexer("[a, b]=[c, d]")
    parser = Parser(lexer)
    parser.stat()

if __name__ == '__main__':
    main()