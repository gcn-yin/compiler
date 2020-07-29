class LCVariable:

    def __init__(self, name):
        self.name = name

    def replace(self, name, replacement):
        if self.name == name:
            return replacement
        else:
            return self

    def callable(self):
        return False

    def reducible(self):
        return False

    def __str__(self):
        return str(self.name)


class LCFunction:

    def __init__(self, parameter, body):
        self.parameter = parameter
        self.body = body

    def replace(self, name, replacement):
        if self.parameter == name:
            return self
        else:
            return LCFunction(
                self.parameter,
                self.body.replace(name, replacement)
            )

    def call(self, argument):
        return self.body.replace(self.parameter, argument)

    def callable(self):
        return True

    def reducible(self):
        return False

    def __str__(self):
        return "=> " + str(self.parameter) + " { " + str(self.body) + " }"


class LCCall:

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def replace(self, name, replacement):
        return LCCall(
            self.left.replace(name, replacement),
            self.right.replace(name, replacement)
        )

    def callable(self):
        return False

    def reducible(self):
        return self.left.reducible() or \
               self.right.reducible() or \
               self.left.callable()

    def reduce(self):
        if self.left.reducible():
            return LCCall(self.left.reduce(), self.right)
        elif self.right.reducible():
            return LCCall(self.left, self.right.reduce())
        else:
            return self.left.call(self.right)

    def __str__(self):
        return str(self.left) + "[" + str(self.right) + ']'


if __name__ == '__main__':
    increment = LCFunction(
        'n',
        LCFunction(
            'p',
            LCFunction(
                'x',
                LCCall(
                    LCVariable('p'),
                    LCCall(
                        LCCall(
                            LCVariable('n'),
                            LCVariable('p')
                        ),
                        LCVariable('x')
                    )
                )
            )
        )
    )
    add = LCFunction(
        'm',
        LCFunction(
            'n',
            LCCall(
                LCCall(
                    LCVariable('n'),
                    increment
                ),
                LCVariable('m')
            )
        )
    )
    one = LCFunction(
        'p',
        LCFunction(
            'x',
            LCCall(
                LCVariable('p'),
                LCVariable('x')
            )
        )
    )
    expression = LCCall(
        LCCall(
            add,
            one
        ),
        one
    )
    while expression.reducible():
        print(expression)
        expression = expression.reduce()
        print(expression)
    print(expression)