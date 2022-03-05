import Node
import Token

current = 0
tokens = None

#토큰이 있는지 확인하기 위해 생성된 함수. 토큰화 할때 코드의 형식이 맞지 않는 경우를 대비
def skipCurrent(kind):
    global current
    global tokens

    if tokens[current].kind != kind:
        print('Error : skipCurrent - nead ', end =' ')
        print(Token.toString(kind))

def skipCurrentIf(kind):
    global current
    global tokens

    if tokens[current].kind != kind:
        return False
    
    current += 1
    return True

##########################################################################

def parseNullLiteral():
    skipCurrent(Token.Kind.NullLiteral)
    result = Node.NullLiteral()
    return result

def parseBooleanLiteral():
    global current
    global tokens

    result = Node.BooleanLiteral()

    result.value = tokens[current].kind == Token.Kind.TrueLiteral
    current += 1
    return result

def parseNumberLiteral():
    global current
    global tokens

    result = Node.NumberLiteral()

    result.value = int(tokens[current].string)
    skipCurrent(Token.Kind.NumberLiteral)
    return result

def parseStringLiteral():
    global current
    global tokens

    result = Node.StringLiteral()

    result.value = tokens[current].string
    skipCurrent(Token.Kind.StringLiteral)
    return result

def parseListLiteral():
    global current
    global tokens

    result = Node.ArrayLiteral()
    skipCurrent(Token.Kind.LeftBraket)
    if tokens[current].kind != Token.Kind.RightBraket:
        while True:
            result.values.append(parseExpression())
            if skipCurrentIf(Token.Kind.Comma): continue
            break
    skipCurrent(Token.Kind.RightBraket)

    return result

def parseMapLiteral():
    global current
    global tokens

    result = Node.MapLiteral()
    skipCurrent(Token.Kind.LeftBrace)
    if tokens[current].kind != Token.Kind.RightBrace:
        while True:
            name = tokens[current].string
            skipCurrent(Token.Kind.StringLiteral)
            skipCurrent(Token.Kind.Colon)
            value = parseExpression()
            result.values[name] = value
            if skipCurrentIf(Token.Kind.Comma): continue
            break
    skipCurrent(Token.Kind.RightBrace)

    return result

def parseIdentifier():
    global current
    global tokens

    result = Node.GetVariable()
    result.name = tokens[current].string
    skipCurrent(Token.Kind.Identifier)
    return result

def parseInnerExpression():
    skipCurrent(Token.Kind.LeftParen)
    result = parseExpression()
    skipCurrent(Token.Kind.RightParen)
    return result

def parseCall(sub):
    global current
    global tokens

    result = Node.Call()
    result.sub = sub
    skipCurrent(Token.Kind.LeftParen)
    if tokens[current].kind != Token.Kind.RightParen:
        while True:
            result.arguments.append(parseExpression())
            if skipCurrentIf(Token.Kind.Comma): continue
            break
    skipCurrent(Token.Kind.RightParen)
    return result

def parseElement(sub):
    result = Node.GetElement()
    result.sub = sub
    skipCurrent(Token.Kind.LeftBraket)
    
    result.index = parseExpression()
    skipCurrent(Token.Kind.RightBraket)

    return result


def parsePostfix(sub):
    global current
    global tokens

    while True:
        kind = tokens[current].kind
        if kind == Token.Kind.LeftParen:
            sub = parseCall(sub)
            break
        if kind == Token.Kind.LeftBraket:
            sub = parseElement(sub)
            break
        else:
            return sub


def parseOperand():
    global current
    global tokens

    result = ''
    kind = tokens[current].kind
    if kind == Token.Kind.NullLiteral: result = parseNullLiteral()
    elif kind == Token.Kind.TrueLiteral or \
        kind == Token.Kind.FalseLiteral: result = parseBooleanLiteral()
    elif kind == Token.Kind.NumberLiteral: result = parseNumberLiteral()
    elif kind == Token.Kind.StringLiteral: result = parseStringLiteral()
    elif kind == Token.Kind.LeftBraket: result = parseListLiteral()
    elif kind == Token.Kind.LeftBrace: result = parseMapLiteral()
    elif kind == Token.Kind.Identifier: result = parseIdentifier()
    elif kind == Token.Kind.LeftParen: result = parseInnerExpression()

    return parsePostfix(result)

#전위 연산자
def parseUnary():
    global current
    global tokens

    operators = {
        Token.Kind.Add,
        Token.Kind.Subtract
    }

    while tokens[current] in operators:
        result = Node.Unary()
        current += 1 # instead skipCurrent()
        result.sub = parseUnary()
        #Expression*
        return result
    
    #Expression*
    return parseOperand()

def parseArithmetic2():
    global current
    global tokens

    operators = {
        Token.Kind.Multiply,
        Token.Kind.Divide,
        Token.Kind.Modulo
    }
    result = parseUnary()
    while tokens[current].kind in operators:
        temp = Node.Arithmetic()
    
        temp.kind = tokens[current].kind
        current += 1
        temp.lhs = result
        temp.rhs = parseUnary()
        result = temp

    return result

def parseArithmetic1():
    global current
    global tokens

    operators = {
        Token.Kind.Add,
        Token.Kind.Subtract
    }
    result = parseArithmetic2()

    while tokens[current].kind in operators:
        temp = Node.Arithmetic()

        temp.kind = tokens[current].kind
        current += 1
        temp.lhs = result
        temp.rhs = parseArithmetic2()
        
        result = temp
    
    return result

def parseRelational():
    global current
    global tokens

    operators = {
        Token.Kind.Equal,
        Token.Kind.NotEqual,
        Token.Kind.LessThan,
        Token.Kind.GreaterThan,
        Token.Kind.LessOrEqual,
        Token.Kind.GreaterOrEqual
    }
    result = parseArithmetic1()

    while tokens[current].kind in operators:
        temp = Node.Arithmetic()

        temp.kind = tokens[current].kind
        current += 1
        temp.lhs = result
        temp.rhs = parseArithmetic1()
        result = temp

    return result

def parseAnd():
    result = parseRelational()

    while skipCurrentIf(Token.Kind.LogicalAnd):
        temp = Node.And()

        temp.lhs = result
        temp.rhs = parseRelational()
        result = temp

    return result

def parseOr():
    result = parseAnd()

    while skipCurrentIf(Token.Kind.LogicalOr):
        temp = Node.Or()

        temp.lhs = result
        temp.rhs = parseAnd()   
        result = temp

    return result

def parseAssignment():
    global current
    global tokens

    result = parseOr()

    if tokens[current].kind != Token.Kind.Assignment:
        return result
    skipCurrent(Token.Kind.Assignment)

    getVariable = None
    if getVariable == Node.GetVariable.dynamic_cast(result):
        result = Node.SetVariable()
        result.name = getVariable.name
        result.value = parseAssignment()
        return result



def parseExpression():
    # return Expresiion*
    return parseAssignment()

def parseVariable():
    global current
    global tokens

    result = Node.Variable()
    skipCurrent(Token.Kind.Variable)
    result.name = tokens[current].string
    skipCurrent(Token.Kind.Identifier)
    skipCurrent(Token.Kind.Assignment)
    result.expressions = parseExpression()

    if result.expressions is None:
        print('변수 선언에 초기화식이 없습니다')
        exit(1)

    skipCurrent(Token.Kind.Semicolon)
    return result

def parseFor():
    global current
    global tokens

    result = Node.For()
    skipCurrent(Token.Kind.For)
    result.variable = Node.Variable()
    result.variable.name = tokens[current].string
    skipCurrent(Token.Kind.Identifier)
    skipCurrent(Token.Kind.Assignment)
    
    result.variable.expressions = parseExpression()
    if result.variable.expressions is None:
        print('for 문에 초기화식이 없습니다')
        exit(1)
    skipCurrent(Token.Kind.Comma)
    result.condition = parseExpression()
    if result.condition is None:
        print('for 문에 조건식이 없습니다.')
        exit(1)
    skipCurrent(Token.Kind.Comma)
    result.expression = parseExpression()
    if result.expression is None:
        print('for 문에 증감식이 없습니다.')
        exit(1)
    
    skipCurrent(Token.Kind.LeftBrace)
    result.block = parseBlock()
    skipCurrent(Token.Kind.RightBrace)

    #return For*
    return result

def parseIf():
    global current
    global tokens

    result = Node.If()
    skipCurrent(Token.Kind.If)
    while True:
        condition = parseExpression()
        if condition is None:
            print('If 문에 조건식이 없습니다.')
            exit(1)
        result.conditions.append(condition)
        skipCurrent(Token.Kind.LeftBrace)
        result.blocks.append(parseBlock())
        skipCurrent(Token.Kind.RightBrace)
        if skipCurrentIf(Token.Kind.Elif): continue
        break
    if skipCurrentIf(Token.Kind.Else):
        skipCurrent(Token.Kind.LeftBrace)
        result.elseBlock = parseBlock()
        skipCurrent(Token.Kind.RightBrace)
    
    return result

def parsePrint():
    global current
    global tokens

    result = Node.Print()
    result.lineFeed = tokens[current].kind == Token.Kind.PrintLine
    current += 1
    
    if tokens[current].kind != Token.Kind.Semicolon:
        while True:
            result.arguments.append(parseExpression())
            if skipCurrentIf(Token.Kind.Comma): continue
            break
    skipCurrent(Token.Kind.Semicolon)
    return result

def parseReturn():
    result = Node.Return()
    skipCurrent(Token.Kind.Return)

    result.expression = parseExpression()
    if result.expression is None:
        print('result 문에 식이 없습니다.')
        exit(1)

    skipCurrent(Token.Kind.Semicolon)    
    return result

def parseBreak():
    result = Node.Break()
    skipCurrent(Token.Kind.Break)
    skipCurrent(Token.Kind.Semicolon)

    return result

def parseContinue():
    result = Node.Continue()
    skipCurrent(Token.Kind.Continue)
    skipCurrent(Token.Kind.Semicolon)
    
    return result

def parseExpressionStatement():
    result = Node.ExpressionStatement()
    result.expression = parseExpression()
    skipCurrent(Token.Kind.Semicolon)

    return result

def parseBlock():
    global current
    global tokens

    result = []

    while tokens[current].kind != Token.Kind.RightBrace:
        kind = tokens[current].kind
        if kind == Token.Kind.Variable: result.append(parseVariable())
        elif kind == Token.Kind.For: result.append(parseFor())
        elif kind == Token.Kind.If: result.append(parseIf())
        elif kind == Token.Kind.Print or kind == Token.Kind.PrintLine: 
            result.append(parsePrint())
        elif kind == Token.Kind.Return: result.append(parseReturn())
        elif kind == Token.Kind.Break: result.append(parseBreak())
        elif kind == Token.Kind.Continue: result.append(parseContinue())
        elif kind == Token.Kind.EndOfToken:
            print('parseBlock Error : EndOfToken 이 RightBrace 토큰보다 먼저 생성되었습니다.')
            exit(1)
        #default
        else: result.append(parseExpressionStatement())

    #return vector<Statement*> result
    return result

def parseFunction():
    global current
    global tokens

    result = Node.Function()

    skipCurrent(Token.Kind.Function)
    result.name = tokens[current].string
    skipCurrent(Token.Kind.Identifier)
    skipCurrent(Token.Kind.LeftParen)
    if tokens[current].kind != Token.Kind.RightParen:
        while True:
            result.parameters.append(tokens[current].string)
            skipCurrent(Token.Kind.Identifier)
            if skipCurrentIf(Token.Kind.Comma): continue
            break
    skipCurrent(Token.Kind.RightParen)
    skipCurrent(Token.Kind.LeftBrace)
    result.block = parseBlock()

    #return Function
    return result

def parse(tokenss):
    global current
    global tokens

    tokens = tokenss

    result = Node.Program()

    while tokens[current] != Token.Kind.EndOfToken:
        kind = tokens[current].kind
        if kind == Token.Kind.Function:
            result.functions.append(parseFunction())
        else:
            print('Error : parse')
            exit(1)

    return result


