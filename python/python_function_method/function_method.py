class Token:
    """Token"""
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
    COLON = 4
    LPARENTH = 5
    RPARENTH = 6
    KEYWORD = 7
    token_names = ['n/a', '<EOF>', 'NAME', 'COMMA', 'COLON', 'LPARENTH', 'RPARENTH', 'KEYWORD']
    keywords = ['def', 'self']
    name_str = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')


    def __init__(self, input):
        self.input = input
        self.point = 0
        self.current = input[self.point]

    def consume(self):
        self.point += 1
        if self.point >= len(self.input):
            self.current = None
        else:
            self.current = self.input[self.point]
    
    def match(self, x):
        if self.current == x:
            self.consume()
        else:
            raise Exception("expcetion" + x + "; found" + self.current)

    def get_token_name(self, x):
        return Lexer.token_names[x]

    def next_token(self):
        while self.current:
            if self.current == ' ' or self.current == '\n' or self.current == '\r' or self.current == '\t':
                self.white_space()
            elif self.current == ',':
                self.consume()
                return Token(Lexer.COMMA, ",")
            elif self.current == ':':
                self.consume()
                return Token(Lexer.COLON, ":")
            elif self.current == '(':
                self.consume()
                return Token(Lexer.LPARENTH, '(')
            elif self.current == ')':
                self.consume()
                return Token(Lexer.RPARENTH, ')')
            elif self.current == 'd' or self.current == 's':
                return self.keyword()
            elif self.current in Lexer.name_str:
                return self.name()
        return Token(Lexer.EOF, '<EOF>')

    def keyword(self):
        _keyword = ''
        if self.current == 's':
            _keyword += self.current
            self.consume()
            if self.current == 'e':
                _keyword += self.current
                self.consume()
                if self.current == 'l':
                    _keyword += self.current
                    self.consume()
                    if self.current == 'f':
                        _keyword += self.current
                        self.consume()
                        return Token(Lexer.KEYWORD, _keyword)
                    else:
                        raise Exception("KEYWORD type not found: " + _keyword)
                else:
                    raise Exception("KEYWORD type not found: " + _keyword)
            else:
                raise Exception("KEYWORD type not found: " + _keyword)
        elif self.current == 'd':
            _keyword += self.current
            self.consume()
            if self.current == 'e':
                _keyword += self.current
                self.consume()
                if self.current == 'f':
                    _keyword += self.current
                    self.consume()
                    return Token(Lexer.KEYWORD, _keyword)
                else:
                    raise Exception("KEYWORD type not found: " + _keyword)
            else:
                raise Exception("KEYWORD type not found: " + _keyword)
        else:
            raise Exception("KEYWORD type not found: " + _keyword)

    def name(self):
        _name = ''
        while self.current in Lexer.name_str:
            _name += self.current
            self.consume()
        return Token(Lexer.NAME, _name)

    def white_space(self):
        while self.current == ' ' or self.current == '\t' or self.current == '\n' or self.current == '\r':
            self.consume()


class Parser:
    """Backtracking Parser"""
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

    def python_def(self):
        if self.speculate_stat_alt1():
            self.classdef()
            self.match(Lexer.EOF)
        elif self.speculate_stat_alt2():
            self.funcdef()
            self.match(Lexer.EOF)            
        else:
            raise Exception("expecting stat found " + str(self.LT(1)))

    def speculate_stat_alt1(self):
        success = True
        self.mark()
        try:
            self.classdef()
            self.match(Lexer.EOF)
        except Exception as e:
            success = False
        self.release()
        return success

    def speculate_stat_alt2(self):
        success = True
        self.mark()
        try:
            self.funcdef()
            self.match(Lexer.EOF)
        except Exception as e:
            success = False
        self.release()
        return success

    def classdef(self):
        self.match(Lexer.KEYWORD)
        self.match(Lexer.NAME)
        self.match(Lexer.LPARENTH)
        self.match(Lexer.KEYWORD)
        self.match(Lexer.COMMA)
        self.match(Lexer.NAME)
        self.match(Lexer.RPARENTH)
        self.match(Lexer.COLON)

    def funcdef(self):
        self.match(Lexer.KEYWORD)
        self.match(Lexer.NAME)
        self.match(Lexer.LPARENTH)
        self.match(Lexer.NAME)
        self.match(Lexer.RPARENTH)
        self.match(Lexer.COLON)        

        

def main():
    lexer = Lexer('def foo(args):')
    parser = Parser(lexer)
    parser.python_def()


if __name__ == '__main__':
    main()
