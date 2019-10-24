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
    'System.out.println': 'PRINT',
    'length': 'LENGTH',
    'true': 'TRUE',
    'false': 'FALSE',
    'this': 'THIS',
    'new': 'NEW',
    'null': 'NULL',
}

tokens = [
             "WHITESPACE",
             "COMMENTARIO",
             "E_PARENTESES",
             "D_PARENTESES",
             "E_COLCHETES",
             "D_COLCHETES",
             "E_CHAVES",
             "D_CHAVES",
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
             "OP_DIVIDE",
             "OP_AND",
             "OP_NAO",
             "ID",
             "NUMBER"
         ] + list(palavras_reservadas.values())

t_E_PARENTESES = r'\('
t_D_PARENTESES = r'\)'
t_E_COLCHETES = r'\['
t_D_COLCHETES = r'\]'
t_E_CHAVES = r'\{'
t_D_CHAVES = r'\}'
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
t_OP_DIVIDE = r'/'
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
    r'System\.out\.println'
    t.type = palavras_reservadas.get(t.value, 'PRINT')
    return t

def t_error(t):
    print('Charactere Inválido' % t.value[0])
    t.type = t.value[0]
    t.value = t.value[0]
    t.lexer.skip(1)
    return t

def t_COMMENT(t):
    r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
    pass


def t_WHITESPACE(t):
    r'\s'
    pass


arquivoEntrada = Path("entrada.txt").read_text()

lex = lexer.lex()
lex.input(arquivoEntrada)

while True:
    token = lex.token()
    if not token:
        break
    print(token)