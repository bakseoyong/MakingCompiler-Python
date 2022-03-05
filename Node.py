
class Program():
    functions = []

class Statement():
    def print():
        print('Statement')

class Expression():
    def print():
        print('Expression')

class Function(Statement):
    name = ''
    parameters = []
    block = []

    def print():
        print('Functions')

class Variable(Statement):
    name = ''
    expressions = None

    def print():
        print('Variable')

#전위 연산자
class Unary(Expression):
    kind = None
    sub = None
    
    def print():
        print('Unary')

class NullLiteral(Expression):
    def print():
        print('NullLiteral')

class BooleanLiteral(Expression):
    value = False

    def print():
        print('BooleanLiteral')

class NumberLiteral(Expression):
    value = 0
    
    def print():
        print('NumberLiteral')

class StringLiteral(Expression):
    value = ''
    
    def print():
        print('StringLiteral')

class ArrayLiteral(Expression):
    values = []
    
    def print():
        print('ArrayLiteral')

class MapLiteral(Expression):
    values = dict()
    
    def print():
        print('MapLiteral')

class GetVariable(Expression):
    name = ''

    def dynamic_cast(self, result):
        self.name = result.name
    
    def print():
        print('GetVariable')

class SetVariable(Expression):
    name = ''
    value = None

    def print():
        print('SetVariable')

class Call(Expression):
    sub = None
    arguments = []

    def print():
        print('Call')

class GetElement(Expression):
    sub = None
    index = None
    
    def print():
        print('GetElement')

class Arithmetic(Expression):
    kind = None
    lhs = None
    rhs = None
    
    def print():
        print('Arithmetic')

class And(Expression):
    lhs = None
    rhs = None
    
    def print():
        print('And')

class Or(Expression):
    lhs = None
    rhs = None

    def print():
        print('Or')

class For(Statement):
    varaible = None
    condition = None
    expression = None
    block = []

    def print():
        print('For')

class If(Statement):
    conditions = []
    blocks = []
    elseBlock = []
    
    def print():
        print('If')

class Print(Statement):
    lineFeed = False
    arguments = []

    def print():
        print('Print')
    
class Return(Statement):
    expression = None

    def print():
        print('Return')
    
class Break(Statement):
    def print():
        print('Break')

class Continue(Statement):
    def print():
        print('Continue')

class ExpressionStatement(Statement):
    expression = None

    def pirnt():
        print('Expression')