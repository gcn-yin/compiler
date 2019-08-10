class Number:
    def __init__(self, value):
        self.value = value

    def reducible(self):
        return False

    def __str__(self):
        num_str = str(self.value)
        return num_str

class Add:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def reduce(self, env):
        if self.left.reducible():
            return Add(self.left.reduce(env), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce(env))
        else:
            return Number(self.left.value + self.right.value)

    def __str__(self):
        add_str = "(" + str(self.left) + " + " + str(self.right) + ")"
        return add_str

class Multiply:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def reduce(self, env):
        if self.left.reducible():
            return Add(self.left.reduce(env), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce(env))
        else:
            return Number(self.left.value * self.right.value)

    def __str__(self):
        mul_str = "(" + str(self.left) + " * " + str(self.right) + ")"
        return mul_str

class Boolean:
    def __init__(self, value):
        self.value = value

    def reducible(self):
        return False

    def __str__(self):
        return str(self.value)

class LessThan:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def __str__(self):
        return "(" + str(self.left) + " < " + str(self.right) + ")"

    def reduce(self, env):
        if self.left.reducible():
            return LessThan(self.left.reduce(env), self.right)
        elif self.right.reducible():
            return LessThan(self.left, self.right.reduce(env))
        else:
            return Boolean(self.left.value < self.right.value)

class Variable:
    def __init__(self, name):
        self.name = name

    def reducible(self):
        return True

    def reduce(self, env):
        return env[self.name]

    def __str__(self):
        return str(self.name)

class Assign:
    def __init__(self, name, exp):
        self.name = name
        self.exp = exp

    def reducible(self):
        return True    

    def reduce(self, env):
        if self.exp.reducible():
            return [Assign(self.name, self.exp.reduce(env)), env]
        else:
            env[self.name] = self.exp
            return [DoNothing(), env]

    def __str__(self):
        return self.name + " = " + str(self.exp)

class DoNothing:
    def __str__(self):
        return 'do-nothing'

    def reducible(self):
        return False

    def __eq__(self, other_statement):
        return isinstance(other_statement, DoNothing)

class If:
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def reducible(self):
        return True

    def reduce(self, env):
        if self.condition.reducible():
            return [If(self.condition.reduce(env), self.consequence, self.alternative), env]
        else:
            if self.condition.value == True:
                return [self.consequence, env]
            elif self.condition.value == False:
                return [self.alternative, env]

    def __str__(self):
        if_str = "if (" + str(self.condition) + ") " + \
                "{ " + str(self.consequence) + " } else { " + \
                str(self.alternative) + " }"
        return if_str

class Machine:
    def __init__(self, stat, env):
        self.stat= stat
        self.env = env

    def step(self):
        self.stat, self.env = self.stat.reduce(self.env)

    def run(self):
        while self.stat.reducible():
            print(self.stat)
            print_dict(self.env)
            self.step()
        print(self.stat)
        print_dict(self.env)

def print_dict(dict):
    dict_str = '{'
    for pair in dict.items():
        dict_str += str(pair[0]) + ": " + str(pair[1])
        dict_str += ', '
    dict_str += '}'
    print(dict_str)

def main():
    machine = Machine(If(Variable('x'), Assign('y', Number(1)), Assign('y', Number(2))), {'x': Boolean(True)})
    machine.run()

if __name__ == '__main__':
    main()