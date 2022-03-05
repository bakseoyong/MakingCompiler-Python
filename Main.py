import Scanner
import Parser

sourceCode = """
function main() {
        print 'Hello, World!';
    }
"""

tokenList = Scanner.scan(sourceCode)
syntaxTree = Parser.parse(tokenList)

print(len(tokenList))

for token in tokenList:
    print(token)