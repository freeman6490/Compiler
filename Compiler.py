from ply import lex, yacc

tokens = ['NUMBER', 'VAR', 'EQUAL',
    'SEMICOL',
    'PLUS',
    'MINUS']

reserved = {'begin': 'BEGIN',
            'end': 'END', 'print': 'PRINT', 'repeat': 'REPEAT'}

tokens += reserved.values()

t_EQUAL = r'\='
t_SEMICOL = r';'
t_ignore = ' \t'
t_PLUS = r'\+'
t_MINUS = r'\-'


def t_NUMBER(token):
    r'\d+'
    try:
        token.value = int(token.value)
    except ValueError:
        print(f"Integer value too large: {t.value}")
        token.value = 0
    return token


def t_VAR(token):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if token.value in reserved:
        token.type = reserved[token.value]
    return token


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character {t.value[0]!r} on line {t.lexer.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()


# Parsing
def p_program(p):
    'program : BEGIN stmt_list END'
    p[0] = f'int main(){{\n{p[2]}\n}}'


def p_stmt_list(p):
    '''stmt_list : stmt SEMICOL stmt_list'''
    p[0] = '{};\n{}'.format(p[1], p[3])


def p_stmt_last(p):
    '''stmt_list : stmt SEMICOL'''
    p[0] = '{};\n'.format(p[1])


def p_stmt(p):
    '''stmt : VAR EQUAL expression'''
    p[0] = '{} = {}'.format(p[1], p[3])

def p_print(p):
    '''stmt : PRINT factor'''
    p[0] = f'cout << {p[2]} << end1'

def p_repeat(p):
    '''stmt : REPEAT NUMBER BEGIN stmt_list END'''
    p[0] = f'for (int i = 0; i < {p[2]}; i++) ' \
           f'{p[4]}'

def p_expression(p):
    '''expression : factor PLUS expression
                  | factor MINUS expression'''

    p[0] = f'{p[1]} {p[2]} {p[3]}'


def p_expression_last(p):
    '''expression : factor'''
    p[0] = f'{p[1]}'


def p_factor(p):
    '''factor : NUMBER
              | VAR'''
    p[0] = f'{p[1]}'


def p_error(t):
    if t is None:  # lexer error
        return

    print(f"Syntax Error: {t.value!r}")


parser = yacc.yacc()

if __name__ == "__main__":
    result = parser.parse('''begin
                                x = 10; 
                                y = 20;
                                repeat 100 begin
                                    a = x + 10;
                                    b = y + x + 100;
                                    print a;
                                end;
                                    print x;
                             end''')

    print(result)
