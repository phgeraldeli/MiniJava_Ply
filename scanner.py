import ply.lex as lexer
from pathlib import Path

palavras_reservadas = {
    'boolean': 'BOOLEAN',
    'class': 'CLASS',
    'extends': 'EXTENDS',
    'public': 'PUBLIC',
    'static': 'STATIC',
    'void': 'VOID',
    'main': 'MAIN',
    'String': 'STRING',
    'return': 'RETURN',
    'int': 'INT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'length': 'LENGTH',
    'true': 'TRUE',
    'false': 'FALSE',
    'this': 'THIS',
    'new': 'NEW',
    'null': 'NULL',
}

tokens = [
            "PRINT",
             "WHITESPACE",
             "COMMENTARIO",
             "EPARENTESE",
             "DPARENTESE",
             "ECOLCHETE",
             "DCOLCHETE",
             "ECHAVE",
             "DCHAVE",
             'SEMICOLON',
             'VIRGULA',
             'PONTO',
             "OP_ASSIGN",
             "OP_MAIOR",
             "OP_MENOR",
             "OP_MAIOR_IGUAL",
             "OP_MENOR_IGUAL",
             "OP_IGUAL",
             "OP_NAO_IGUAL",
             "OP_MENOS",
             "OP_MAIS",
             "OP_MULTIPLICA",
             "OP_AND",
             "OP_NAO",
             "ID",
             "NUMBER"
         ] + list(palavras_reservadas.values())

t_EPARENTESE = r'\('
t_DPARENTESE = r'\)'
t_ECOLCHETE = r'\['
t_DCOLCHETE = r'\]'
t_ECHAVE = r'\{'
t_DCHAVE = r'\}'
t_SEMICOLON = r';'
t_VIRGULA = r'\,'
t_PONTO = r'\.'
t_OP_ASSIGN = r'='
t_OP_MAIOR = r'>'
t_OP_MENOR = r'<'
t_OP_MAIOR_IGUAL = r'>='
t_OP_MENOR_IGUAL = r'<='
t_OP_IGUAL = r'=='
t_OP_NAO_IGUAL = r'!='
t_OP_MENOS = r'\-'
t_OP_MAIS = r'\+'
t_OP_MULTIPLICA = r'\*'
t_OP_AND = r'&&'
t_OP_NAO = r'!'


def t_NUMBER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = palavras_reservadas.get(t.value, 'ID')
    return t

def t_PRINT(t):
    r'(System\.out\.println)'
    t.type = palavras_reservadas.get(t.value, 'PRINT')
    return t

def t_error(t):
    print('Charactere Inválido' % t.value[0])
    t.type = t.value[0]
    t.value = t.value[0]
    t.lexer.skip(1)
    return t

def t_COMMENT(t):
    r'((/\*([^*]|[\r\n])|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
    pass


def t_WHITESPACE(t):
    r'\s'
    pass

precedence = (
    ('left', "OP_ASSIGN"),
    ('left', 'OP_AND'),
    ('left', 'OP_IGUAL', 'OP_NAO_IGUAL'),
    ('left', 'OP_MAIOR_IGUAL', 'OP_MAIOR', 'OP_MENOR_IGUAL', 'OP_MENOR'),
    ('left', 'OP_MENOS', 'OP_MAIS'),
    ('left', 'OP_MULTIPLICA'),
    ('nonassoc', 'OP_NAO')
)

arquivoEntrada = Path("entrada.txt").read_text()

lex = lexer.lex()
lex.input(arquivoEntrada)

while True:
    token = lex.token()
    if not token:
        break
    print(token)