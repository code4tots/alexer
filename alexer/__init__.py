"""
Dead simple lexer without a lot of flexibility.
"""

class Token(object):
    def __init__(self, type_, full_text, location, value = None):
        self.type = type_
        self.full_text = full_text
        self.location = location
        self.value = value
    
    def __repr__(self):
        return '(%s,%s)' % (self.type, self.value)

class Lexer(object):
    def __init__(self, symbols, keywords):
        from re import compile as rec, escape as esc
        
        self.regex_token_pairs = tuple(
            (type_, rec(regex)) for type_, regex in
                tuple(
                    ('KEYWORD', keyword + r'(?!\w)')
                    for keyword in keywords
                ) + (
                    ('STRING',
                        r'\"(?:\\\"|[^"])*\"' + r'|'
                        r"\'(?:\\\'|[^'])*\'"),
                    ('FLOAT',   r'\-?\d+\.\d*'),
                    ('INT',     r'\-?\d+'),
                    ('NAME',    r'\w+')
                ) + tuple(
                    ('SYMBOL', esc(symbol))
                    for symbol in symbols
                )
            )
        self.space_re = rec(r'[ \t]*(?:\#[^\n]*)?')
        self.empty_lines_re = rec(r'(?:(?:[ \t]*(?:\#[^\n]*)?)(?:\n|\Z))*')
        self.err_re = rec(r'[^\s]*')
        
    def lex(self, string):
        s = string
        p = self.regex_token_pairs
        c = self.space_re
        e = self.empty_lines_re
        i = e.match(s).end()
        d = ['']
        while i < len(s):
            m = c.match(s,i)
            ind = m.group()
            if ind == d[-1]:
                pass
            elif ind.startswith(d[-1]):
                d.append(ind)
                yield Token('INDENT', s, i)
            elif ind in d:
                while ind != d[-1]:
                    d.pop()
                    yield Token('DEDENT', s, i)
            else:
                raise SyntaxError('invalid indent')
            i = m.end()
            while i < len(s) and s[i] != '\n':
                for type_, regex in p:
                    m = regex.match(s,i)
                    if m is not None:
                        yield Token(type_, s, i, m.group())
                        i = m.end()
                        break
                else:
                    t = self.err_re.match(s,i).group()
                    raise SyntaxError('unrecognized token %r' % (t,))
                i = c.match(s,i).end()
            yield Token('NEWLINE', s, i)
            i = e.match(s,i).end()
        while len(d) > 1:
            d.pop()
            yield Token('DEDENT', s, len(s))
        yield Token('END', s, len(s))