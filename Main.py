import Scanner
import Parser
import Generator
import Machine

sourceCode = """
function main() {
        var a = 5; 
        print 'Hello, World!';
    }
"""

tokenList = Scanner.scan(sourceCode)
syntaxTree = Parser.parse(tokenList)
objectCode = Generator.generate(syntaxTree)
Machine.execute(objectCode)

"""print(len(tokenList))

for token in tokenList:
    print(token)"""
