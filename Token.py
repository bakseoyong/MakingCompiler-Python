from enum import Enum
import collections

# instead Struct
Token = collections.namedtuple("Token", "kind string")

class Kind(Enum):
    Unknown = "#unknown"
    EndOfToken = "#EndOfToken"
    NullLiteral = "null"
    TrueLiteral = "true"
    FalseLiteral = "false"
    NumberLiteral = "#Number"
    StringLiteral = "#String"
    Identifier = "#identifier"
    Function = "function"
    Return = "return"
    Variable = "var"
    For = "for"
    Break = "break" 
    Continue = "continue"
    If = "if"
    Elif = "elif"
    Else = "else"
    Print = "print"
    PrintLine = "printLine"
    LogicalAnd = "and"
    LogicalOr = "or"
    Assignment = "="
    Add = "+"
    Subtract = "-" 
    Multiply = "*"
    Divide = "/"
    Modulo = "%"
    Equal = "=="
    NotEqual = "!="
    LessThan = "<"
    GreaterThan = ">"
    LessOrEqual = "<=" 
    GreaterOrEqual = ">="
    Comma = ","
    Colon = ":"
    Semicolon = ";"
    LeftParen = "("
    RightParen = ")"
    LeftBrace = "{"
    RightBrace = "}"
    LeftBraket = "["
    RightBraket = "]"

kindToString = {
    "#unknown" : Kind.Unknown,
    "#EndOfToken" : Kind.EndOfToken,
    "null" : Kind.NullLiteral,
    "true" : Kind.TrueLiteral,
    "false" : Kind.FalseLiteral,
    "#Number" : Kind.NumberLiteral,
    "#String" : Kind.StringLiteral,
    "#identifier" : Kind.Identifier,
    "function" : Kind.Function,
    "return" : Kind.Return,
    "var" : Kind.Variable,
    "for" : Kind.For,
    "break" : Kind.Break,
    "continue" : Kind.Continue,
    "if" : Kind.If,
    "elif" : Kind.Elif,
    "else" : Kind.Else,
    "print" : Kind.Print,
    "printLine" : Kind.PrintLine,
    "and" : Kind.LogicalAnd,
    "or" : Kind.LogicalOr,
    "=" : Kind.Assignment,
    "+" : Kind.Add,
    "-" : Kind.Subtract,
    "*" : Kind.Multiply,
    "/" : Kind.Divide,
    "%" : Kind.Modulo,
    "==" : Kind.Equal,
    "!=" : Kind.NotEqual,
    "<" : Kind.LessThan,
    ">" : Kind.GreaterThan,
    "<=" : Kind.LessOrEqual,
    ">=" : Kind.GreaterOrEqual,
    "," : Kind.Comma,
    ":" : Kind.Colon,
    ";" : Kind.Semicolon,
    "(" : Kind.LeftParen,
    ")" : Kind.RightParen,
    "{" : Kind.LeftBrace,
    "}" : Kind.RightBrace,
    "[" : Kind.LeftBraket,
    "]" : Kind.RightBraket
}

def toKind(string):
    try:
        if kindToString[string]:
            return kindToString[string]
    except KeyError:
        return Kind.Unknown