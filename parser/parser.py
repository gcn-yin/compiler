class Element:
    def parse(self, lexer, res):
        pass

    def match(self, lexer):
        pass


class Tree(Element):

    def __init__(self, parser):
        self.parser = parser

    def parse(self, lexer, res):
        res.append(self.parser.parse(lexer))

    def match(self, lexer):
        return self.parser.match(lexer)


class OrTree(Element):

    def __init__(self, parsers):
        self.parsers = parsers

    def parse(self, lexer, res):
        p = self.choose(lexer)
        if not p:
            raise Exception() # todo
        else:
            res.append(p.parse(lexer))

    def match(self, lexer):
        return self.choose(lexer) is not None

    def choose(self, lexer):
        for parser in self.parsers:
            if parser.match(lexer):
                return parser
        return None

    def insert(self, parser):
        self.parsers = self.parsers.insert(0, parser)


class Repeat(Element):

    def __init__(self, parser, once):
        self.parser = parser
        self.only_once = once

    def parse(self, lexer, res):
        while self.parser.match(lexer):
            t = self.parser.parse(lexer)
            # if type(t) = ASTList or t.num_children > 0:
            #     res.append(t) todo
            if self.only_once:
                break

    def match(self, lexer):
        return self.parser.match(lexer)