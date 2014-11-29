from alexer import PlyLexer
from ply import yacc

lexer = PlyLexer({
  '-' : 'MINUS',
  '=' : 'EQUAL',
  '(' : 'LPAR',
  ')' : 'RPAR'},
  ['while'])

lexer.input("""

x = 10 - 5

# while x
#   print(x)
#   x = x - 1

""")

tokens = lexer.tokens

def p_expression(p):
  """expression : expression MINUS expression
                | expression EQUAL expression
                | INT
                | FLOAT
                | STRING
                | NAME
                | expression LPAR expression RPAR
                | expression NEWLINE"""
  p[0] = [p[i] for i in range(1, len(p)) if p[i] is not None]

def p_all(p):
  """all : expression END"""
  p[0] = p[1]

start = 'all'

parser = yacc.yacc()

result = parser.parse(lexer=lexer)
print(result) # [['x'], '=', [['10'], '-', [['5']]]]
