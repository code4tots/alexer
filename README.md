alexer
======

The lexer with very few options that supports Python style indentation.

Example usage:

python```
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


"""
   KEYWORD          while        13
      NAME           just        19
      NAME           true        24
   NEWLINE           None        41
    INDENT           None        42
      NAME          print        46
    SYMBOL              (        52
      NAME            add        53
       INT              1        57
     FLOAT            2.3        59
    SYMBOL              )        62
    STRING 'hello world!'        64
   NEWLINE           None        78
    DEDENT           None        80
       END           None        80
"""

```
Token types:

    KEYWORD
    STRING
    FLOAT
    INT
    NAME
    SYMBOL
    INDENT
    DEDENT
    NEWLINE
    END

