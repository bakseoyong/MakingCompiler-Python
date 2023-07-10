
class Instruction():
    Exit = "Exit"
    Call = "Call"
    Alloca = "Alloca"
    Return = "Return"

    Jump = "Jump"
    ConditionJump = "ConditionJump"

    Print = "Print"
    PrintLine = "PrintLine"

    LogicalOr = "LogicalOr"
    LogicalAnd = "LogicalAnd"

    Equal = "Equal"
    NotEqual = "NotEqual"
    LessThan = "LessThan"
    GreaterThan = "GreaterThan"
    LessOrEqual = "LessOrEqual"
    GreaterOrEqual = "GreaterOrEqual"

    Add = "Add"
    Subtract = "Subtract"
    Multiply = "Multiply"
    Divide = "Divide"
    Modulo = "Modulo"

    Absolute = "Absolute"
    ReverseSign = "ReverseSign"
    GetElement = "GetElement"
    SetElement = "SetElement"
    GetGlobal = "GetGlobal"
    SetGlobal = "SetGlobal"
    GetLocal = "GetLocal"
    SetLocal = "SetLocal"

    PushNull = "PushNull"
    PushBoolean = "PushBoolean"
    PushNumber = "PushNumber"
    PushString = "PushString"
    PushArray = "PushArray"
    PushMap = "PushMap"
    PopOperand = "PopOperand"


stringToInstruction = {
    'Exit' : Instruction.Exit,
    'Call' : Instruction.Call,
    'Alloca' : Instruction.Alloca,
    'Return' : Instruction.Return,
    'Jump' : Instruction.Jump,
    'ConditionJump' : Instruction.ConditionJump,
    'Print' : Instruction.Print,
    'PrintLine' : Instruction.PrintLine,
    'LogicalOr' : Instruction.LogicalOr,
    'LogicalAnd' : Instruction.LogicalAnd,
    'Equal' : Instruction.Equal,
    'NotEqual' : Instruction.NotEqual,
    'LessThan' : Instruction.LessThan,
    'GreaterThan' : Instruction.GreaterThan,
    'LessOrEqual' : Instruction.LessOrEqual,
    'GreaterOrEqual' : Instruction.GreaterOrEqual,
    'Add' : Instruction.Add,
    'Subtract' : Instruction.Subtract,
    'Multiply' : Instruction.Multiply,
    'Divide' : Instruction.Divide,
    'Modulo' : Instruction.Modulo,
    'Absolute' : Instruction.Absolute,
    'ReverseSign' : Instruction.ReverseSign,
    'GetElement' : Instruction.GetElement,
    'SetElement' : Instruction.SetElement,
    'GetGlobal' : Instruction.GetGlobal,
    'SetGlobal' : Instruction.SetGlobal,
    'GetLocal' : Instruction.GetLocal,
    'SetLocal' : Instruction.SetLocal,
    'PushNull' : Instruction.PushNull,
    'PushBoolean' : Instruction.PushBoolean,
    'PushNumber' : Instruction.PushNumber,
    'PushString' : Instruction.PushString,
    'PushArray' : Instruction.PushArray,
    'PushMap' : Instruction.PushMap,
    'PopOperand' : Instruction.PopOperand
}