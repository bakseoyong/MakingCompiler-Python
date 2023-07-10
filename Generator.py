from dis import Instruction
import Constant
import Code
import Node
import Token

codeList = []
functionTable = dict()
localSize = 0
#list<map<string, size_t>> symbolStack
symbolStack = []
#vector<size_t> offsetStack
offsetStack = []
continueStack = []
breakStack = []


def writeCode(instruction, operand):
    global codeList

    codeList.append({instruction, operand})
    return len(codeList) - 1

def writeCode1(instruction):
    global codeList
    codeList.append({instruction})
    return len(codeList) - 1

def initBlock():
    global localSize, offsetStack, symbolStack

    localSize = 0
    offsetStack.append(0)
    #emplace_front() - 스택 공간을 할당해주는것 같은데 파이썬에서는 어떻게 해야될까
    symbolStack.insert(0, dict())

def popBlock():
    global offsetStack, symbolStack

    offsetStack.pop()
    symbolStack.pop(0)

def pushBlock():
    global symbolStack, offsetStack

    symbolStack.insert(0, dict())
    offsetStack.append(offsetStack[-1])

def setLocal(name):
    global localSize, offsetStack, symbolStack
    #제대로 된건지..
    symbolStack[0][name] = offsetStack[-1]
    offsetStack[-1] += 1
    localSize = max(localSize, offsetStack[-1])

def getLocal(name):
    for symbolTable in symbolStack:
        if name in symbolTable:
            return symbolTable[name]

    #return SIZE_MAX
    return Constant.SIZE_MAX

def patchOperand(codeIndex, operand):
    global codeList

    codeList[codeIndex].operand = operand

def patchAddress(codeIndex):
    codeList[codeIndex].operand = len(codeList)

def generateFunction(node):
    global functionTable, localSize

    functionTable[node.name] = len(codeList)
    temp = writeCode1(Code.Instruction.Alloca)
    initBlock()
    for name in node.parameters:
        setLocal(name)
    for n in node.block:
        nodeToGenerate(n)

    popBlock()
    patchOperand(temp, localSize)
    writeCode1(Code.Instruction.Return)

def generatePrint(node):
    for argument in reversed(node.arguments):
        nodeToGenerate(argument)
    writeCode(Code.Instruction.Print, len(node.arguments))
    if node.lineFeed:
        writeCode1(Code.Instruction.PrintLine)

def generateVariable(node):
    setLocal(node.name)
    nodeToGenerate(node.expression)
    writeCode(Code.Instruction.SetLocal, getLocal(node.name))
    writeCode1(Code.Instruction.PopOperand)

def generateNumberLiteral(node):
    writeCode(Code.Instruction.PushNumber, node.value)

def generateBooleanLiteral(node):
    writeCode(Code.Instruction.PushBoolean, node.value)

def generateStringLiteral(node):
    writeCode(Code.Instruction.PushString, node.value)

def generateNullLiteral(node):
    writeCode1(Code.Instruction.PushNull)

def generateContinue(node):
    global continueStack

    if len(continueStack) == 0: return
    jumpCode = writeCode1(Code.Instruction.Jump)
    continueStack[-1].append(jumpCode)

def generateBreak(node):
    global breakStack

    if len(breakStack) == 0: return
    jumpCode = writeCode1(Code.Instruction.Jump)
    breakStack[-1].append(jumpCode)


def generateVariable(variable):
    setLocal(variable.name)
    nodeToGenerate(variable.expression)
    writeCode(Code.Instruction.SetLocal)
    writeCode1(Code.Instruction.PopOperand)

def generateFor(node):
    global breakStack, continueStack, codeList

    breakStack.insert(0, dict())
    continueStack.insert(0, dict())
    pushBlock()

    nodeToGenerate(node.variable)
    jumpAddress = len(codeList)
    nodeToGenerate(node.condition)
    conditionJump = writeCode1(Code.Instruction.ConditionJump)

    for n in node.block:
        nodeToGenerate(n)
    continueAddress = len(codeList)
    nodeToGenerate(node.expression)
    writeCode1(Code.Instruction.PopOperand)
    writeCode(Code.Instruction.Jump, jumpAddress)
    patchAddress(conditionJump)
    popBlock()
    
    for jump in continueStack[-1]:
        patchOperand(jump, continueAddress)
    continueStack.pop()

    for jump in breakStack[-1]:
        patchAddress(jump)
    breakStack.pop()

def generateIf(node):
    jumpList = []
    for i in range(0, len(node.conditions)):
        nodeToGenerate(node.conditions[i])
        conditionJump = writeCode1(Code.Instruction.ConditionJump)
        pushBlock()
        for n in node.blocks[i]:
            nodeToGenerate(n)
        popBlock()
        jumpList.append(writeCode1(Code.Instruction.Jump))
        patchAddress(conditionJump)
    if len(node.elseBlock) != 0:
        pushBlock()
        for n in node.elseBlock:
            nodeToGenerate(n)
        popBlock()
    for jump in jumpList:
        patchAddress(jump)

def generateReturn(node):
    nodeToGenerate(node.expression)
    writeCode1(Code.Instruction.Return)

def generateExpressionStatement(node):
    nodeToGenerate(node.expression)
    writeCode1(Code.Instruction.PopOperand)

def generateOr(node):
    nodeToGenerate(node.lhs)
    logicalOr = writeCode1(Code.Instruction.LogicalOr)
    nodeToGenerate(node.rhs)
    patchAddress(logicalOr)

def generateAnd(node):
    nodeToGenerate(node.lhs)
    logicalAnd = writeCode1(Code.Instruction.LogicalAnd)
    nodeToGenerate(node.rhs)
    patchAddress(logicalAnd)

def generateCall(node):
    for i in range(len(node.arguments), 0, -1):
        nodeToGenerate(node.arguments[i - 1])
    nodeToGenerate(node.sub)
    writeCode1(Code.Instruction.Call, len(node.arguments))

def generateGetElement(node):
    nodeToGenerate(node.sub)
    nodeToGenerate(node.index)
    writeCode1(Code.Instruction.GetElement)

def generateSetElement(node):
    nodeToGenerate(node.value)
    nodeToGenerate(node.sub)
    nodeToGenerate(node.index)
    writeCode1(Code.Instruction.SetElement)

def generateArrayLiteral(node):
    for i in range(len(node.value), 0, -1):
        nodeToGenerate(node.values(i - 1))
    writeCode(Code.Instruction.PushArray, len(node.values))

def generateMapLiteral(node):
    for key, value in node.values:
        writeCode(Code.Instruction.PushString, key)
        nodeToGenerate(value)
    writeCode(Code.Instruction.PushMap, len(node.values))

def generateGetVariable(node):
    if getLocal(node.name) == Constant.SIZE_MAX:
        writeCode(Code.Instruction.GetGlobal, node.name)
    else:
        writeCode(Code.Instruction.GetGlobal, getLocal(node.name))

def generateSetVariable(node):
    nodeToGenerate(node.value)
    if getLocal(node.name) == Constant.SIZE_MAX:
        writeCode(Code.Instruction.SetGlobal, node.name)
    else:
        writeCode(Code.Instruction.SetLocal, getLocal(node.name))

def generateRelational(node):
    instructions = {
        Token.Kind.Equal : Code.Instruction.Equal,
        Token.Kind.NotEqual : Code.Instruction.NotEqual,
        Token.Kind.LessThan : Code.Instruction.LessThan,
        Token.Kind.GreaterThan : Code.Instruction.GreaterThan,
        Token.Kind.LessOrEqual : Code.Instruction.LessOrEqual,
        Token.Kind.GreaterOrEqual : Code.Instruction.GreaterOrEqual
    }
    nodeToGenerate(node.lhs)
    nodeToGenerate(node.rhs)
    writeCode1(instructions[node.kind])

def generateArithmetic(node):
    instructions = {
        Token.Kind.Add : Code.Instruction.Add,
        Token.Kind.Subtract : Code.Instruction.Subtract,
        Token.Kind.Multiply : Code.Instruction.Multiply,
        Token.Kind.Divide : Code.Instruction.Divide,
        Token.Kind.Modulo : Code.Instruction.Modulo
    }
    nodeToGenerate(node.lhs)
    nodeToGenerate(node.rhs)
    writeCode1(instructions[node.kind])

def generateUnary(node):
    instructions = {
        Token.Kind.Add : Code.Instruction.Absolute,
        Token.Kind.Subtract : Code.Instruction.ReverseSign
    }
    nodeToGenerate(node.sub)
    writeCode1(instructions[node.kind])

def nodeToGenerate(node):
    if type(node) == type(Node.Function()): generateFunction(node)
    elif type(node) == type(Node.Print()): generatePrint(node)
    elif type(node) == type(Node.Variable()): generateVariable(node)
    elif type(node) == type(Node.NumberLiteral()): generateNumberLiteral(node)
    elif type(node) == type(Node.BooleanLiteral()): generateBooleanLiteral(node)
    elif type(node) == type(Node.StringLiteral()): generateStringLiteral(node)
    elif type(node) == type(Node.NullLiteral()): generateNullLiteral(node)
    elif type(node) == type(Node.Continue()): generateContinue(node)
    elif type(node) == type(Node.Break()): generateBreak(node)
    elif type(node) == type(Node.Return()): generateReturn(node)
    elif type(node) == type(Node.For()): generateFor(node)
    elif type(node) == type(Node.If()): generateIf(node)
    elif type(node) == type(Node.ExpressionStatement()): 
        generateExpressionStatement(node)
    elif type(node) == type(Node.Or()): generateOr(node)
    elif type(node) == type(Node.And()): generateAnd(node)
    elif type(node) == type(Node.Call()): generateCall(node)
    elif type(node) == type(Node.GetElement()): generateGetElement(node)
    elif type(node) == type(Node.SetElement()): generateSetElement(node)
    elif type(node) == type(Node.ArrayLiteral()): generateArrayLiteral(node)
    elif type(node) == type(Node.MapLiteral()): generateMapLiteral(node)
    elif type(node) == type(Node.GetVariable()): generateGetVariable(node)
    elif type(node) == type(Node.SetVariable()): generateSetVariable(node)
    elif type(node) == type(Node.Relational()): generateRelational(node)
    elif type(node) == type(Node.Unary()): generateUnary(node)


def generate(program):
    global codeList
    global functionTable

    codeList.clear()
    functionTable.clear()

    writeCode(Code.Instruction.GetGlobal, "main")
    writeCode(Code.Instruction.Call, 0) #static_cast<size_t>(0)
    writeCode1(Code.Instruction.Exit)

    for node in program.functions:
        nodeToGenerate(node)
        #node.generate()

    # return dict
    return {codeList, functionTable}
