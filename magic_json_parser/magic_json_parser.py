class Token:
    """Token"""
    def __init__(self, type, text):
        self.type = type
        self.text = text
    
    def __str__(self):
        return "<'" + self.text + "'," + Lexer.token_name[self.type] + ">"


class Lexer:
    """LL(1)"""
    EMPTY = 1
    COMMA = 2
    COLON = 3
    L_BRACE = 4
    R_BRACE = 5
    L_BRACKET = 6
    R_BRACKET = 7
    NUMBER = 8
    STRING = 9
    BOOL = 10
    NULL = 11
    EOF_TYPE = 12
    EQUALS = 13
    token_name = ['n/a', 'EMPTY', 'COMMA', 'COLON', 'L_BRACE', 'R_BRACE', 'L_BRACKET',
                  'R_BRACKET', 'NUMBER', 'STRING', 'BOOL', 'NULL', 'EOF_TYPE', 'EQUALS']
    string_content = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()_+[]\{}|;':,./<>?*-+ \n\t\r")

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
            elif self.current == '[':
                self.consume()
                return Token(Lexer.L_BRACKET, "[")
            elif self.current == ']':
                self.consume()
                return Token(Lexer.R_BRACKET, "]")
            elif self.current == '{':
                self.consume()
                return Token(Lexer.L_BRACE, "{")
            elif self.current == '}':
                self.consume()
                return Token(Lexer.R_BRACE, "}")
            elif self.current == '=':
                self.consume()
                return Token(Lexer.EQUALS, '=')
            elif self.current == '"':
                return self.string()
            elif self.current == 't' or self.current == 'f':
                return self.bool()
            elif self.current == 'n':
                return self.null()
            elif self.is_number():
                return self.number()
        return Token(Lexer.EOF_TYPE, "<EOF>")

    def null(self):
        _null = ''
        if self.current == 'n':
            _null += self.current
            self.consume()
            if self.current == 'u':
                _null += self.current
                self.consume()
                if self.current == 'l':
                    _null += self.current
                    self.consume()
                    if self.current == 'l':
                        _null += self.current
                        self.consume()
                        return Token(Lexer.NULL, _null)
                    else:
                        raise Exception("NULL type not found: " + _null)
                else:
                    raise Exception("NULL type not found: " + _null)
            else:
                raise Exception("NULL type not found: " + _null)
        else:
            raise Exception("NULL type not found: " + _null)
                                                
    def bool(self):
        _bool = ''
        if self.current == 't':
            _bool += self.current
            self.consume()
            if self.current == 'r':
                _bool += self.current
                self.consume()
                if self.current == 'u':
                    _bool += self.current
                    self.consume()
                    if self.current == 'e':
                        _bool += self.current
                        self.consume()
                        return Token(Lexer.BOOL, _bool)
                    else:
                        raise Exception("BOOL type not found: " + _bool)
                else:
                    raise Exception("BOOL type not found: " + _bool)
            else:
                raise Exception("BOOL type not found: " + _bool)
        elif self.current == 'f':
            _bool += self.current
            self.consume()
            if self.current == 'a':
                _bool += self.current
                self.consume()
                if self.current == 'l':
                    _bool += self.current
                    self.consume()
                    if self.current == 's':
                        _bool += self.current
                        self.consume()
                        if self.current == 'e':
                            _bool += self.current
                            self.consume()
                            return Token(Lexer.BOOL, _bool)
                        else:
                            raise Exception("BOOL type not found: " + _bool)
                    else:
                        raise Exception("BOOL type not found: " + _bool)
                else:
                    raise Exception("BOOL type not found: " + _bool)
            else:
                raise Exception("BOOL type not found: " + _bool)
        else:
            raise Exception("BOOL type not found: " + _bool)
            
    def string(self):
        _string = ''
        _string += self.current
        self.consume()
        while self.is_content():
            _string += self.current
            self.consume()
        if self.current == '"':
            _string += self.current
            self.consume()
            return Token(Lexer.STRING, _string)
        else:
            raise Exception('expcetion: " not found')

    def is_content(self):
        return self.current in Lexer.string_content
 
    def number(self):
        _number = ''
        _number += self.current
        self.consume()
        while self.is_number():
            _number += self.current
            self.consume()
        if not self.is_number():
            return Token(Lexer.NUMBER, _number)

    def is_number(self):
        return self.current in list('0123456789')

    def get_token_name(self, token_type):
        return Lexer.token_name[token_type]

    def white_space(self):
        while self.current == ' ' or self.current == '\t' or self.current == '\n' or self.current == '\r':
            self.consume()


class Parser:
    """LL(k)"""
    def __init__(self, input, k):
        self.input = input
        self.k = k
        self.point = 0
        self.lookahead = [0 for i in range(0, k)]
        for i in range(0, self.k):
            self.consume()

    def consume(self):
        self.lookahead[self.point] = self.input.next_token()
        self.point = (self.point + 1) % self.k

    def lookahead_token(self, i):
        return self.lookahead[(self.point + i -1) % self.k]

    def lookahead_type(self, i):
        return self.lookahead_token(i).type

    def match(self, x):
        if self.lookahead_type(1) == x:
            self.consume()

    def run(self):
        if self.lookahead_type(1) == Lexer.L_BRACKET:
            self.list()
        elif self.lookahead_type(1) == Lexer.L_BRACE:
            self.object()

    def list(self):
        self.match(Lexer.L_BRACKET)
        self.elements()
        self.match(Lexer.R_BRACKET)

    def elements(self):
        self.element()
        while self.lookahead_type(1) == Lexer.COMMA:
            self.match(Lexer.COMMA)
            self.element()
    
    def element(self):
        if self.lookahead_type(1) == Lexer.STRING and self.lookahead_type(2) == Lexer.EQUALS:
            self.match(Lexer.STRING)
            self.match(Lexer.EQUALS)
            self.match(Lexer.STRING)
        elif self.lookahead_type(1) == Lexer.NUMBER:
            self.match(Lexer.NUMBER)
        elif self.lookahead_type(1) == Lexer.STRING:
            self.match(Lexer.STRING)
        elif self.lookahead_type(1) == Lexer.BOOL:
            self.match(Lexer.BOOL)
        elif self.lookahead_type(1) == Lexer.NULL:
            self.match(Lexer.NULL)
        elif self.lookahead_type(1) == Lexer.L_BRACKET:
            self.list()
        elif self.lookahead_type(1) == Lexer.L_BRACE:
            self.object()

    def object(self):
        self.match(Lexer.L_BRACE)
        self.pair()
        while self.lookahead_type(1) == Lexer.COMMA:
            self.match(Lexer.COMMA)
            self.pair()
        self.match(Lexer.R_BRACE)

    def pair(self):
        self.match(Lexer.STRING)
        self.match(Lexer.COLON)
        self.value()

    def value(self):
        if self.lookahead_type(1) == Lexer.STRING:
            self.match(Lexer.STRING)
        elif self.lookahead_type(1) == Lexer.NUMBER:
            self.match(Lexer.NUMBER)
        elif self.lookahead_type(1) == Lexer.BOOL:
            self.match(Lexer.BOOL)
        elif self.lookahead_type(1) == Lexer.NULL:
            self.match(Lexer.NULL)
        elif self.lookahead_type(1) == Lexer.L_BRACE:
            self.object()
        elif self.lookahead_type(1) == Lexer.L_BRACKET:
            self.list()

def main():
    lexer = Lexer('{"a": 1, "b": true, "c": "see", "d": [1, 2, 3], "e"="f"}')
    parser = Parser(lexer, 2)
    parser.run()

if __name__ == '__main__':
    main()