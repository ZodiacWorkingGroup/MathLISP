import ply.lex as lex

tokens = [
    'FUNC',
    'INT',
    'FLOAT',
    'SPINT',
    'SPFLOAT',
    'STR',
    'OPAREN',
    'CPAREN',
    'BOOL'
]


class SpecialNum:
    def __init__(self, val, const):
        self.val = val
        self.const = const

    def __repr__(self):
        return repr(self.val)+self.const


def t_BOOL(t):
    """[tT](rue|RUE)|[fF](alse|ALSE)"""
    t.value = t.value[0].upper() == 'T'
    return t


def t_SPFLOAT(t):
    """[0-9]+\.[0-9]+[^0-9.()\s]"""
    t.value = SpecialNum(float(t.value[:-1]), t.value[-1])
    return t


def t_SPINT(t):
    """
    0b[01]+[^0-9a-fA-F.()\s]|
    0q[0-3]+[^0-9a-fA-F.()\s]|
    0o[0-7]+[^0-9a-fA-F.()\s]|
    0x[0-9a-f]+[^0-9a-fA-F.()\s]|
    0x[0-9A-F]+[^0-9a-fA-F.()\s]|
    [0-9]+[^0-9a-fA-F.()\s]
    """
    if t.value[:2] == '0b':
        t.value = SpecialNum(int(t.value[2:-1], 2), t.value[-1])

    elif t.value[:2] == '0q':
        t.value = SpecialNum(int(t.value[2:-1], 4), t.value[-1])

    elif t.value[:2] == '0o':
        t.value = SpecialNum(int(t.value[2:-1], 8), t.value[-1])

    elif t.value[:2] == '0x':
        t.value = SpecialNum(int(t.value[2:-1], 16), t.value[-1])

    else:
        t.value = SpecialNum(int(t.value[:-1]), t.value[-1])

    return t


def t_FLOAT(t):
    """[0-9]+\.[0-9]+"""
    t.value = float(t.value)
    return t


def t_INT(t):
    """
    0b[01]+|
    0q[0-3]+|
    0o[0-7]+|
    0x[0-9a-f]+|
    0x[0-9A-F]+|
    [0-9]+
    """
    if t.value[:2] == '0b':
        t.value = int(t.value[2:], 2)

    elif t.value[:2] == '0q':
        t.value = int(t.value[2:], 4)

    elif t.value[:2] == '0o':
        t.value = int(t.value[2:], 8)

    elif t.value[:2] == '0x':
        t.value = int(t.value[2:], 16)

    else:
        t.value = int(t.value)

    return t


def t_STR(t):
    '''"[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'''
    t.value = bytes(t.value[1:-1], 'utf-8').decode('unicode-escape')
    return t


def t_FUNC(t):
    r"""[^()0-9\s"]+"""
    return t

t_OPAREN = r'\('
t_CPAREN = r'\)'

t_ignore = ' \t\n'


def t_error(t):
    raise SyntaxError('Invalid character: '+t.value)

lexer = lex.lex()

if __name__ == '__main__':
    lexer.input(input())
    for x in lexer:
        print(x)
