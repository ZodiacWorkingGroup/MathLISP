import ply.yacc as yacc
from lex import tokens


class func:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '{'+self.name+'}'


def p_expression_s(p):
    """expression : OPAREN expression CPAREN"""
    # print('s-expression: '+str(p[2]))
    p[0] = [p[2]]


def p_expression_empty(p):
    """expression : OPAREN CPAREN"""
    # print('Empty expression!')
    p[0] = None


def p_expression_list(p):
    """expression : expression expression"""
    # print('Expression list: '+repr([x for x in p]))
    p[1].extend(p[2])
    p[0] = p[1]


def p_expression_unit(p):
    """expression : INT
                  | FLOAT
                  | STR
                  | BOOL
                  | SPINT
                  | SPFLOAT
                  """
    # print('Unit expression: '+repr([x for x in p]))
    p[0] = [p[1]]


def p_expression_func(p):
    """expression : FUNC"""
    p[0] = [func(p[1])]


def p_error(p):
    raise SyntaxError('Unrecognized symbol encountered: '+p.value)

parser = yacc.yacc(tabmodule="tm")

if __name__ == '__main__':
    print(parser.parse(input())[0])
