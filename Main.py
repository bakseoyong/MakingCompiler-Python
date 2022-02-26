import Scanner

sourceCode = """
function main() {
        print 'Hello, World!';
    }
"""

tokenList = Scanner.scan(sourceCode)
print(len(tokenList))

for token in tokenList:
    print(token)