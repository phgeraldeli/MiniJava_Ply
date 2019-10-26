import ply.yacc as yacc
from scanner import tokens
from pathlib import Path
from ply.lex import LexToken
##########
# Parser para a linguagem mini-java
#########


## metodos descrevendo as produções da linguagem 

## PROG : MAIN CLASSE
def p_prog(p):
    'prog : main classes'
    p[0] = ('prog', p[1:]) 

def p_main(p):
    'main : CLASS ID ECHAVE PUBLIC STATIC VOID MAIN EPARENTESE STRING ECOLCHETE DCOLCHETE ID DPARENTESE ECHAVE cmd DCHAVE DCHAVE'
    p[0] = ('main', p[1:])


# multiplas classes
def p_classes(p):
    '''
    classes : empty 
               | classes classe
    '''
    p[0] = ('classes',p[1:])

def p_classe(p):
    '''
    classe : CLASS ID EXTENDS ID ECHAVE variaveis metodos DCHAVE 
           | CLASS ID ECHAVE variaveis metodos DCHAVE
    '''
    p[0] = ('classe', p[1:])    

#multiplas variáveis
def p_variaveis(p):
    '''
    variaveis : empty 
              | variaveis variavel
    '''
    p[0] = ('variaveis', p[1:])

def p_variavel(p):
    '''
    variavel : tipo ID SEMICOLON
    '''
    p[0] = ('variavel', p[1:])

#multiplos métodos
def p_metodos(p):
    '''
    metodos : empty 
            | metodos metodo
    '''
    p[0] = ('metodos', p[1:])

def p_metodo(p):
    '''
    metodo : PUBLIC tipo ID EPARENTESE params DPARENTESE ECHAVE variaveis cmds RETURN exp SEMICOLON DCHAVE
            | PUBLIC tipo ID EPARENTESE DPARENTESE ECHAVE variaveis cmds RETURN exp SEMICOLON DCHAVE
    '''
    p[0] = ('metodo', p[1:])


def p_params(p):
    '''
    params : tipo ID sequenciaparams
    '''
    p[0] = ('params', p[1:])

def p_sequenciaparams(p):
    '''
    sequenciaparams : sequenciaparams SEMICOLON tipo ID 
                    | empty

    '''
    p[0] = ('sequenciaparams', p[1:])

def p_tipo(p):
    '''
    tipo : INT ECOLCHETE DCOLCHETE 
            | BOOLEAN 
            | INT
            | ID 
    '''
    p[0] = ('tipo', p[1:])


def p_cmds(p):
    '''cmds : cmds cmd 
            | empty
    '''
    p[0] = ('cmds', p[1:])

def p_cmd(p):
    '''
    cmd : ECHAVE cmds DCHAVE
            | IF EPARENTESE exp DPARENTESE cmd  
            | IF EPARENTESE exp DPARENTESE cmd ELSE cmd
            | WHILE EPARENTESE exp DPARENTESE cmd
            | PRINT EPARENTESE exp DPARENTESE SEMICOLON
            | ID OP_ASSIGN exp SEMICOLON 
            | ID ECOLCHETE exp DCOLCHETE OP_ASSIGN exp SEMICOLON
    ''' 
    p[0] = ('cmd', p[1:])

def p_exp(p):
    '''
    exp : exp OP_AND rexp
        | rexp
    '''
    p[0] = ('exp', p[1:])

def p_rexp(p):
    '''
    rexp : rexp OP_MENOR aexp 
            | rexp OP_IGUAL aexp
            | rexp OP_NAO_IGUAL aexp
            | aexp
    '''
    p[0] = ('rexp', p[1:])

def p_aexp(p):
    '''
    aexp : aexp OP_MAIS mexp
            | aexp OP_MENOS mexp
            | mexp
    '''
    p[0] = ('aexp', p[1:])

def p_mexp(p):
    '''
    mexp : mexp OP_MULTIPLICA sexp
            | sexp
    '''
    p[0] = ('mexp', p[1:])

def p_sexp(p):
    '''
    sexp : OP_NAO sexp
            | OP_MENOS sexp
            | TRUE
            | FALSE
            | NUMBER
            | NULL
            | NEW INT ECOLCHETE exp DCOLCHETE
            | pexp PONTO LENGTH
            | pexp ECOLCHETE exp DCOLCHETE
            | pexp
    '''
    p[0] = ('sexp', p[1:])

def p_pexp(p):
    '''
    pexp : ID
            | THIS
            | NEW ID EPARENTESE DPARENTESE
            | EPARENTESE exp DPARENTESE
            | pexp PONTO ID
            | pexp PONTO ID EPARENTESE exps DPARENTESE
            | pexp PONTO ID EPARENTESE DPARENTESE
    '''
    p[0] = ('pexp', p[1:])

def p_exps(p):
    'exps : exp sequenciaexp'
    p[0] = ('exps', p[1:])

def p_sequenciaexp(p):
    '''
    sequenciaexp : sequenciaexp VIRGULA exp 
                 | empty
    '''
    p[0] = ('sequenciaexp', p[1:])

    

def p_error(p): 
     if not p:
         print("End of File!")
         return
     else:
         print("Syntax Error : {}".format(p))
     # Read ahead looking for a closing '}'
     while True:
         tok = parser.token()             # Get the next token
         if not tok or tok.type == 'DCHAVE': 
             break
     parser.restart()

def p_empty(p):
    'empty : '
    pass

parser = yacc.yacc(debug=True, method='SLR')
entrada = Path("entrada.txt").read_text()
parserOut = parser.parse(entrada)