from alexer import Lexer

lexer = Lexer(
    symbols = ('(', ')'),
    keywords = ('for', 'while', 'if', 'else'))

tokens = lexer.lex("""

# comments
while just true # some stuff
    print (add 1 2.3) 'hello world!'

""")

for token in tokens:
    print('%10s%15s%10s' % (token.type, token.value, token.location))

