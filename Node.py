
from re import L


class Program():
    def __init__(self, functions):
        self.functions = functions

class Statement():
    def print():
        print('Statement')

class Expression():
    def print():
        print('Expression')

class Function(Statement):
    def __init__(self, name, parameters, block):
        self.name = name
        self.parameters = parameters
        self.block = block

    def print():
        print('Functions')

class Variable(Statement):
    def __init__(self, name, expressions):
        self.name = name
        self.expressions = expressions

    def print():
        print('Variable')

#전위 연산자
class Unary(Expression):
    def __init__(self, kind, sub):
        self.kind = kind
        #Expression*
        self.sub = sub
    
    def print():
        print('Unary')

class NullLiteral(Expression):
    def print():
        print('NullLiteral')

class BooleanLiteral(Expression):
    def __init__(self, value):
        self.value = value

    def print():
        print('BooleanLiteral')

class NumberLiteral(Expression):
    def __init__(self, value):
        self.value = value
    
    def print():
        print('NumberLiteral')

class StringLiteral(Expression):
    def __init__(self, value):
        self.value = value
    
    def print():
        print('StringLiteral')

class ArrayLiteral(Expression):
    def __init__(self, values):
        self.values = values
    
    def print():
        print('ArrayLiteral')

class MapLiteral(Expression):
    def __init__(self, values):
        self.values = values
    
    def print():
        print('MapLiteral')

class GetVariable(Expression):
    def __init__(self, name):
        self.name = name

    def dynamic_cast(self, result):
        self.name = result.name
    
    def print():
        print('GetVariable')

class SetVariable(Expression):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Call(Expression):
    def __init__(self, sub, arguments):
        self.sub = sub
        self.arguments = arguments

    def print():
        print('Call')

class GetElement(Expression):
    def __init__(self, sub, index):
        self.sub = sub
        self.index = index
    
    def print():
        print('GetElement')


class Arithmetic(Expression):
    def __init__(self, kind, lhs, rhs):
        self.kind = kind
        self.lhs = lhs
        self.rhs = rhs
    
    def print():
        print('Arithmetic')

class And(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    
    def print():
        print('And')

class Or(Expression):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def print():
        print('Or')

class For(Statement):
    def __init__(self, variable, condition, expression, block):
        self.variable = variable
        self.condition = condition
        self.expression = expression
        self.block = block

    def print():
        print('For')

class If(Statement):
    def __init__(self, conditions, blocks, elseBlock):
        self.conditions = conditions
        self.blocks = blocks
        self.elseBlock = elseBlock
    
    def print():
        print('If')

class Print(Statement):
    def __init__(self, lineFeed, arguments):
        self.lineFeed = lineFeed
        self.arguments = arguments

    def print():
        print('Print')
    
class Return(Statement):
    def __init__(self, expression):
        self.expression = expression

    def print():
        print('Return')
    
class Break(Statement):
    def print():
        print('Break')

class Continue(Statement):
    def print():
        print('Continue')

class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def pirnt():
        print('Expression')