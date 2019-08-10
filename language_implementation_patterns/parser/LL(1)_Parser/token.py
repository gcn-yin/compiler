from lexer import Lexer

class Token:

    def __init__(self, type, text):
        self.type = type
        self.text = text

    def __str__(self):
        name = Lexer.tokenNames[self.type]
        return '<' + self.text + ',' + name + '>'