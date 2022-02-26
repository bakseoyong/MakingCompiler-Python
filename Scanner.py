from enum import Enum
import collections

#책에서는 포인터였지만 인덱스 값으로 선언
current = 0

#token.py에 있지만 웹에서 코딩이라 임시로 선언
Token = namedtuple("Token", "kind string")

class CharType(Enum):
Unknown = ''
WhiteSpace = ''
NumberLiteral = ''
StringLiteral = ''
IdentifierAndKeyword = ''
OperatorAndPunctuator = ''

def getCharType(char):
if char == ' ' or char == '/t' or char == '/n' or char == '/r':
    return CharType.WhiteSpace
elif char.isdigit():
    return CharType.NumberLiteral
elif char == '\'':
    return CharType.StringLiteral
elif char.isalpha():
    return CharType.IdentifierAndKeyword
elif 33 <= ord(char) and ord(char) and ord(char) != '\'' or
    58 <= ord(char) and ord(char) <= 64 or
    91 <= ord(char) and ord(char) <= 96 or
    123 <= ord(char) and ord(char) <= 126:
    return CharType.OperatorAndpnctuator

def isCharType(char, charType):
    if charType == CharType.NumberLiteral:
        return char.isdigit()
    elif charType == CharType.StringLiteral:
        return char.isalpha()
    elif charType == CharType.IdentifierAndKeyword:
        return char.isalpha() or char.isdigit()
    elif charType == CharType.OperatorAndPunctuator:
        #and 우선순위가 더 높다.
        return ord(char) >= 33 and ord(char) <= 47 or
        ord(char) >= 58 and ord(char) <= 63 or
        ord(char) >= 91 and ord(char) <= 96 or
        ord(char) >= 123 and ord(char) <= 126
    else:
        return False

################################################################################

def scanNumberLiteral(sourceCode):
    string = ''
    while isCharType(sourceCode[current], CharType.NumberLiteral):
        string += sourceCode[current]
        current += 1
    #실수일경우 .이 추가된다
    if sourceCode[current] == '.':
        stirng += '.'
        current += 1
    while isCharType(sourceCode[current], CharType.NumberLiteral):
        string += sourceCode[current]
        current += 1

    #return Token(struct)
    return Token(Kind.NumberLiteral, string)

​

def scanStringLiteral(sourceCode):
    string = ''
    # '로 시작하니까 1 더하기
    current += 1 
    ​
    while isCharType(sourceCode[sourceCode], CharType.StringLiteral):
        string += sourceCode[current]
        current += 1

    #detect '
    if soureCode[current] != '\'':
        print('Error : scanStringLiteral')
        
    current += 1

    return Token(Kind.StringLiteral, string)

​

def scanIdentifierAndKeyword(soureCode):
    string = ''
    ​
    while isCharType(soureCode[soureCode], CharType.IdentifierAndKeyword):
        string += sourceCode[current]
        current += 1

    kind = toKind(string)

    if kind == Kind.Unknown:
        kind = Kind.Identifier

    return Token(kind, string)

​

def scanOperatorAndPunctuator(soureCode):
    string = ''

    while isCharType(soureCode[soureCode], CharType.OperatorAndPunctuator):
        string += sourceCode[current]
        current += 1
    # C의 count함수가 아닌 딕셔너리로 탐색하기 때문에 연산자에 판단에 코드를 작성하지 않아도 된다.
    """
    #C - search operator and punctuator
    while len(string) != 0 and toKind(string) == Kind.Unknown:
        #remove last char
        string = string[:-1]
        current -= 1
    if len(string) == 0:
        print('Error : scanOperatorAndPunctuator')
    """
    if toKind(string) == Kind.Unknown:
        print('Error : scanOperatorAndPunctuator')
        
    return Token(Kind.OperatorAndPunctuator, string)



################################################################################

#parameter - string type
def scan(sourceCode):
    global current
    # token list
    result = []

    current = 0 

    while current < len(sourceCode):
        charType = getCharType(sourceCode[current])
        if charType == CharType.WhiteSpace:
            current += 1
        elif charType == CharType.NumberLiteral:
            result.append(scanNumberLiteral(sourceCode)) 
        elif charType == CharType.StringLiteral:
            result.append(scanStringLiteral(sourceCode))
        elif charType == CharType.IdentifierAndKeyword:
            result.append(scanIdentifierAndKeyword(sourceCode))
        elif charType == CharType.OperatorAndPunctuator:
            #result.append(scanOperatorAndPunctuator(sourceCode))
        else:
            print('Error : scan error')

    result.append(Kind.EndOfToken)

    return result

###################################################################

sourceCode = " "

scan(sourceCode)