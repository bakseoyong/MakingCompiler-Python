import DataType
import Code
from Generator import getLocal

class StackFrame():
    variables = []
    operandStack = []
    instructionPointer = 0

objects = []
globals = {}
callStack = []
builtinFunctionTable = {}

# tuple<vector<Code>, map<string, size_t>> objectCode
def execute(objectCode):
    global globals, objects, callStack
    globals.clear()
    objects.clear()
    callStack.append(dict())
    
    # get<0>(objectCode)
    # get<1>(objectCode)
    codeList = objectCode[0]
    functionTable = objectCode[1]
    while True:
        code = codeList[callStack[-1].instructionPointer]
        #switch
        if code.instruction == Code.Instruction.Exit:
            # 맨 마지막 요소가 startup()
            del callStack[-1]
            return
        elif code.instruction == Code.Instruction.Call:
            operand = popOperand()
            #주소 타입 (size_t)가 맞는지 확인하기 위해 isSize함수를 사용
            #if isSize(operand):
            stackFrame = StackFrame()
            # stackFrame.instructionPointer = toSize(operand)
            stackFrame.instructionPointer = operand

            # ex) Call [2] 라면 2개의 요소를 인자로 받아야 되기 떄문에 code.operand 만큼 반복
            for i in range(0, code.operand):
                stackFrame.variables.append(callStack[-1])
            callStack.append(stackFrame)
            continue

            # 주소 타입이 아닐때
            # pushOperand(nullptr)
            # break
        elif code.instruction == Code.Instruction.Alloca:
            #extraSize = toSize(code.operand)
            extraSize = len(code.operand)
            currentSize = len(callStack[-1].variables)
            #callStack[-1].variables.resize(currentSize + extraSize)
        elif code.instruction == Code.Instruction.Return:
            # 피연산자 스택에 남아있는 값이 없다면 null을 기본값으로 한다.
            result = None
            if len(callStack[-1].operandStack) != 0:
                result = callStack[-1].operandStack[-1]
            del callStack[-1]
            callStack[-1].operandStack.append(result)
            #collectGarbage()
        elif code.instruction == Code.Instruction.Jump:
            callStack[-1].instructionPointer = code.operand
            continue
        elif code.instruction == Code.Instruction.ConditionJump:
            condition = popOperand()
            if condition:
                continue
            callStack[-1].instructionPointer = code.operand
            continue
        elif code.instruction == Code.Instruction.Print:
            for i in range(0, len(code.operand)):
                value = popOperand()
                print(value)
        elif code.insturction == Code.Instruction.PrintLine:
            print()
        elif code.instruction == Code.Instruction.LogicalOr:
            value = popOperand()
            if value:
                pushOperand(value)
                # code.operand가 일반 수 인지 확인 할 필요 있음
                callStack[-1].instructionPointer = len(code.operand)
                continue
        elif code.instruction == Code.Instruction.LogicalAnd:
            value = popOperand()
            if not value:
                pushOperand(value)
                callStack[-1].instructionPointer = len(code.operand)
                continue
        elif code.instruction == Code.Instruction.Equal:
            rValue = popOperand()
            lValue = popOperand()
            if rValue == lValue:
                pushOperand(True)
            else:
                pushOperand(False)
        elif code.instruction == Code.Instruction.NotEqual:
            rValue = popOperand()
            lValue = popOperand()
            if rValue != lValue:
                pushOperand(True)
            else:
                pushOperand(False)
        elif code.instruction == Code.Instruction.LessThan:
            rValue = popOperand()
            lValue = popOperand()
            if lValue < rValue:
                pushOperand(True)
            else:
                pushOperand(False)
        elif code.instruction == Code.Instruction.GreaterThan:
            rValue = popOperand()
            lValue = popOperand()
            if lValue > rValue:
                pushOperand(True)
            else:
                pushOperand(False)
        elif code.instruction == Code.Instruction.LessOrEqual:
            rValue = popOperand()
            lValue = popOperand()
            if lValue <= rValue:
                pushOperand(True)
            else:
                pushOperand(False)
        elif code.instruction == Code.Instruction.GreaterOrEqual:
            rValue = popOperand()
            lValue = popOperand()
            if lValue <= rValue:
                pushOperand(True)
            else:
                pushOperand(False)
        elif code.instruction == Code.Instruction.Add:
            rValue = popOperand()
            lValue = popOperand()
            if type(rValue) == type(lValue):
                pushOperand(lValue + rValue) 
            else:
                pushOperand(0.0)
        elif code.instruction == Code.Instruction.Subtract:
            rValue = popOperand()
            lValue = popOperand()
            if type(rValue) == type(lValue) == type(0):
                pushOperand(lValue - rValue) 
            else:
                pushOperand(0.0)
        elif code.instruction == Code.Instruction.Multiply:
            rValue = popOperand()
            lValue = popOperand()
            if type(rValue) == type(lValue) == type(0):
                pushOperand(lValue * rValue) 
            else:
                pushOperand(0.0)
        elif code.instruction == Code.Instruction.Divide:
            rValue = popOperand()
            lValue = popOperand()
            if type(rValue) == type(lValue) and rValue == 0:
                pushOperand(0.0)
            elif type(rValue) == type(lValue) == type(0):
                pushOperand(lValue / rValue) 
            else:
                pushOperand(0.0)
        elif code.instruction == Code.Instruction.Modulo:
            rValue = popOperand()
            lValue = popOperand()
            if type(rValue) == type(lValue) and rValue == 0:
                pushOperand(0.0)
            elif type(rValue) == type(lValue) == type(0):
                pushOperand(lValue % rValue) 
            else:
                pushOperand(0.0)
        elif code.instruction == Code.Instruction.Absolute:
            value = popOperand()
            if type(value) == type(0):
                pushOperand(abs(value))
            else:
                pushOperand(0.0)
        elif code.instruction == Code.Instruction.ReverseSign:
            value = popOperand()
            if type(value) == type(0):
                pushOperand(value * -1)
            else:
                pushOperand(0.0)
        elif code.instruction == Code.Instruction.GetElement:
            index = popOperand()
            sub = popOperand()
            if type(sub) == type([]) and type(index) == type(0):
                pushOperand(DataType.getValueOfArray(sub, index))
            elif type(sub) == type(dict()) and type(index) == type(''):
                pushOperand(DataType.getValueOfMap(sub, index))
            else:
                pushOperand(None)
        elif code.instruction == Code.Instruction.SetElement:
            index = popOperand()
            sub = popOperand()
            if type(sub) == type([]) and type(index) == type(0):
                DataType.setValueOfArray(sub, index, peekOperand())
            if type(sub) == type(dict()) and type(index) == type(''):
                DataType.setValueOfMap(sub, index, peekOperand())
        elif code.instruction == Code.Instruction.GetGlobal:
            name = code.operand
            # map<string, size_t> functionTable
            if functionTable[name]:
                pushOperand(functionTable[name])
            elif builtinFunctionTable[name]:
                pushOperand(builtinFunctionTable[name])
            elif globals[name]:
                pushOperand(globals[name])
            else:
                pushOperand(None)
        elif code.instruction == Code.Instruction.SetGlobal:
            name = code.operand
            globals[name] = peekOperand()
        # 참조할 지역변수의 오프셋을 인자로 가지므로 현재 스택 프레임의
        # 변수 배열에서 오프셋 위치에 저장돼 있는 값을 피연산자 스택에 넣는다
        elif code.instruction == Code.Instruction.GetLocal:
            index = code.operand
            pushOperand(callStack[-1].variables[index])
        elif code.instruction == Code.Instruction.SetLocal:
            index = code.operand
            callStack[-1].variables[index] = peekOperand()
        elif code.instruction == Code.Instruction.PushNull:
            pushOperand(None)
        elif code.instruction == Code.Insturction.PushBoolean:
            pushOperand(code.operand)
        elif code.instruction == Code.Instruction.PushNumber:
            pushOperand(code.operand)
        elif code.instruction == Code.Instruction.PushString:
            pushOperand(code.operand)
        elif code.instruction == Code.Instruction.PushArray:
            result = []
            # code.operand == 배열의 요소 개수
            for i in range(0, code.operand):
                result.append(popOperand())
            pushOperand(result)
            objects.append(result)
        elif code.instruction == Code.Instruction.PushMap:
            result = dict()
            for i in range(0, code.operand):
                value = popOperand()
                key = popOperand()
                result[key] = value
            pushOperand(result)
            objects.append(result)
        elif code.instruction == Code.Instruction.PopOperand:
            popOperand()
        callStack[-1].instructionPointer += 1


def popOperand():
    global callStack

    # 가장 최근에 삽입된 요소
    value = callStack[-1].operandStack[-1]
    del callStack[-1].operandStack[-1]
    return value

def pushOperand(value):
    global callStack

    callStack[-1].operandStack.append(value)

def peekOperand():
    global callStack

    return callStack[-1].operandStack[-1]

def collectGarbage():
    for stackFrame in callStack:
        for value in stackFrame.operandStack:
            markObject(value)
        for value in stackFrame.variables:
            markObject(value)

def markObject(value):
    if type(value) == type([]):
        #value.

        