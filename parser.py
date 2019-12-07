import ply.yacc as yacc
from scanner import tokens
from pathlib import Path
from ply.lex import LexToken
from codeGenerator import codeGenerator
from AnalizadorSemantico import AnalizadorSemantico
import re


##########
# Parser para a linguagem mini-java
#########

precedence = (
    ('left', 'DPARENTESE'),
    ('left', 'ELSE')
)

## metodos descrevendo as produções da linguagem 

## PROG : MAIN CLASSE
def p_prog(p):
    'prog : main classes'
    p[0] = Node('prog', [ p[1], p[2] ], [])
    # print(p[0].type)

def p_main(p):
    'main : CLASS ID ECHAVE PUBLIC STATIC VOID MAIN EPARENTESE STRING ECOLCHETE DCOLCHETE ID DPARENTESE ECHAVE cmd DCHAVE DCHAVE'
    p[0] = Node('main', [ p[15] ],  [ p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[16], p[17] ])
    # print(p[0].type)

# multiplas classes
def p_classes(p):
    '''
    classes : classes classe 
               | empty 
    '''
    if len(p) == 3:
        p[0] = Node('classes', [ p[1], p[2] ], [ ])
    else:
        p[0]= Node('classes', [ p[1] ], [ ])
    # print(p[0].type)

def p_classe(p):
    '''
    classe : CLASS ID extends_id ECHAVE variaveis metodos DCHAVE
    '''
    p[0] = Node('classe', [ p[3], p[5], p[6] ], [ p[1], p[2], p[4], p[7] ])    
    # print(p[0].type)

def p_extends_id(p):
    '''
    extends_id : EXTENDS ID
               | empty
    '''
    if len(p) == 3:
        p[0] = Node('extends_id', [], [ p[1], p[2] ])
    else:
        p[0] = Node('extends_id', [ p[1] ], [])
    # print(p[0].type)

#multiplas variáveis
def p_variaveis(p):
    '''
    variaveis : variaveis variavel
              | empty
    '''
    if len(p) == 3:
        p[0] = Node('variaveis', [ p[1], p[2] ], [])
    else:
        p[0] = Node('variaveis', [ p[1] ], [])
    # print(p[0].type)
            

def p_variavel(p):
    '''
    variavel : tipo ID SEMICOLON
    '''
    p[0] = Node('variavel', [ p[1] ], [ p[2], p[3] ])
    # print(p[0].type)

#multiplos métodos
def p_metodos(p):
    '''
    metodos : metodos metodo 
            | empty
    '''
    if len(p) == 3:
        p[0] = Node('metodos', [ p[1], p[2] ], [ ])
    else: 
        p[0] = Node('metodos', [ p[1] ], [ ])
    # print(p[0].type)

def p_metodo(p):
    '''
    metodo : PUBLIC tipo ID EPARENTESE params_o DPARENTESE ECHAVE variaveis cmds RETURN exp SEMICOLON DCHAVE
    '''
    p[0] = Node('metodo', [ p[2], p[5], p[8], p[9], p[11] ], [ p[1], p[3], p[4], p[6], p[7], p[10], p[12], p[13] ])
    # print(p[0].type)

def p_params_o(p):
    '''
    params_o : params
             | empty
    '''
    p[0] = Node('params_o', [ p[1] ], [ ])
    # print(p[0].type)

def p_params(p):
    '''
    params : tipo ID sequenciaparams
    '''
    p[0] = Node('params', [ p[1], p[3] ], [ p[2] ])
    # print(p[0].type)

def p_sequenciaparams(p):
    '''
    sequenciaparams : SEMICOLON tipo ID sequenciaparams
                    | empty

    '''
    if len(p) == 5:
        p[0] = Node('sequenciaparams', [ p[2], p[4] ], [ p[1], p[3] ])
    else:    
        p[0] = Node('sequenciaparams', [ p[1] ], [])
    # print(p[0].type)

def p_tipo(p):
    '''
    tipo : INT tipo2 
         | BOOLEAN
         | ID 
    '''
    if len(p) == 3:
        p[0] = Node('tipo', [ p[2] ], [ p[1] ])
    else:    
        p[0] = Node('tipo', [], [ p[1]])
    # print(p[0].type)

def p_tipo2(p):
    '''
    tipo2 : ECOLCHETE DCOLCHETE 
          | empty  
    '''
    if len(p) == 3:
        p[0] = Node('tipo2', [], [ p[1], p[2] ])
    else:
        p[0] = Node('tipo2', [ p[1] ], [ ])
    # print(p[0].type)

def p_cmds(p):
    '''cmds : cmd cmds
            | empty
    '''
    if len(p) == 3:
        p[0] = Node('cmds', [ p[1], p[2] ], [])
    else:
        p[0] = Node('cmds', [ p[1] ], [])
    # print(p[0].type)

def p_cmd(p):
    '''
    cmd :     ECHAVE cmds DCHAVE
            | IF EPARENTESE exp DPARENTESE cmd ELSE cmd
            | IF EPARENTESE exp DPARENTESE cmd
            | WHILE EPARENTESE exp DPARENTESE cmd
            | PRINT EPARENTESE exp DPARENTESE SEMICOLON
            | ID cmd_id
    '''
    if len(p) == 4:
        p[0] = Node('cmd', [ p[2] ], [ p[1], p[3] ])
    elif len(p) == 8:
        p[0] = Node('cmd', [ p[3], p[5], p[7] ], [ p[1], p[2], p[4], p[6] ])
    elif len(p) == 6:
        if p[1] == 'while':
            p[0] = Node('cmd', [ p[3], p[5] ], [ p[1], p[2], p[4] ])
        else:
            p[0] = Node('cmd', [ p[3] ], [ p[1], p[2], p[4], p[5] ])
    else:
        p[0] = Node('cmd', [ p[2] ], [ p[1] ])
    # print(p[0].type)
        
    
def p_cmd_id(p):
    '''
    cmd_id : OP_ASSIGN exp SEMICOLON
           | ECOLCHETE exp DCOLCHETE OP_ASSIGN exp SEMICOLON
    '''
    if len(p) == 4:
        p[0] = Node('cmd_id', [ p[2] ], [ p[1], p[3] ])
    else:
        p[0] = Node('cmd_id', [ p[2], p[5] ], [ p[1], p[3], p[4], p[6] ])
    # print(p[0].type)

def p_exp(p):
    '''
    exp : exp OP_AND rexp
        | rexp
    '''
    if len(p) == 4: 
        p[0] = Node('exp', [ p[1], p[3] ], [ p[2] ])
    else:
        p[0] = Node('exp', [ p[1] ], [])
    # print(p[0].type)

def p_rexp(p):
    '''
    rexp : rexp rexp2
            | aexp
    '''
    if len(p) == 3:
        p[0] = Node('rexp', [ p[1], p[2] ], [])
    else:
        p[0] = Node('rexp', [ p[1] ], [])
    # print(p[0].type)

def p_rexp2(p):
    '''
    rexp2 : OP_MENOR aexp
          | OP_IGUAL aexp
          | OP_NAO_IGUAL aexp
    '''
    p[0] = Node('rexp2', [ p[2] ], [ p[1] ])
    # print(p[0].type)

def p_aexp(p):
    '''
    aexp : aexp OP_MAIS mexp
            | aexp OP_MENOS mexp
            | mexp
    '''
    if len(p) == 4:
        p[0] = Node('aexp', [ p[1], p[3] ], [ p[2] ])
    else:
        p[0] = Node('aexp', [ p[1] ], [])        
    # print(p[0].type)

def p_mexp(p):
    '''
    mexp : mexp OP_MULTIPLICA sexp
            | sexp
    '''
    if len(p) == 4:
        p[0] = Node('mexp', [ p[1], p[3] ], [ p[2] ])
    else:
        p[0] = Node('mexp', [ p[1] ], [])
    # print(p[0].type)

def p_sexp(p):
    '''
    sexp :    OP_NAO sexp
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
    if len(p) == 3:
        p[0] = Node('sexp', [ p[2] ], [ p[1] ])
    elif len(p) == 4:
        p[0] = Node('sexp', [ p[1] ], [ p[2], p[3] ])
    elif len(p) == 5:
        p[0] = Node('sexp', [ p[1], p[3] ], [ p[2], p[4] ])
    elif len(p) == 6:
        p[0] = Node('sexp', [ p[4] ], [ p[1], p[2], p[3], p[5] ])
    else:
        number = re.compile('[0-9]+')
        if (p[1] == 'true') or (p[1] == 'false') or (p[1] == 'null') or (number.match(str(p[1]))):
            p[0] = Node('sexp', [], [ p[1] ])
        else:
            p[0] = Node('sexp', [ p[1] ], [])
    # print(p[0].type)

def p_pexp(p):
    '''
    pexp :    ID
            | THIS
            | NEW ID EPARENTESE DPARENTESE
            | EPARENTESE exp DPARENTESE
            | pexp PONTO ID
            | pexp PONTO ID EPARENTESE exps DPARENTESE
            | pexp PONTO ID EPARENTESE DPARENTESE
    '''
    if len(p) == 2:
        p[0] = Node('pexp', [], [ p[1] ])
    elif len(p) == 4:
        if p[1] == '(':
            p[0] = Node('pexp', [ p[2] ], [ p[1], p[3] ])
        else:
            p[0] = Node('pexp', [ p[1] ], [ p[2], p[3]])
    elif len(p) == 5:
        p[0] = Node('pexp', [], [ p[1], p[2], p[3], p[4] ])
    elif len(p) == 6:
        p[0] = Node('pexp', [ p[1], p[5] ], [ p[2], p[3], p[4], p[6] ])
    elif len(p) == 7:
        p[0] = Node('pexp', [ p[1] ], [ p[2], p[3], p[4], p[5] ])
    # print(p[0].type)

def p_exps(p):
    'exps : exp sequenciaexp'
    p[0] = Node('exps', [ p[1], p[2] ], [])
    # print(p[0].type)

def p_sequenciaexp(p):
    '''
    sequenciaexp : VIRGULA exp sequenciaexp
                 | empty
    '''
    if len(p) == 4:
        p[0] = Node('sequenciaexp', [ p[2], p[3] ], [ p[1] ])
    else:
        p[0] = Node('sequenciaexp', [ p[1] ], [])
    # print(p[0].type)


def p_empty(p):
    'empty : '
    p[0] = Node('empty', [], [])
    # print(p[0].type)

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

class Node:
    def __init__(self,type,children=None,leaf=None):
        self.type = type
        if children:
            self.children = children              
        else:
            self.children = [ ]              
        self.leaf = leaf

def build_tree(current_node, spaces=0):
    if(isinstance(current_node,Node)):     
        leafs = ""    
        leafs += str(current_node.leaf)
        line = ("    "*spaces) + current_node.type + " -> leafs: (" + leafs +")\n"
        file_tree.write(line)
        for child in current_node.children:            
            build_tree(child, spaces+1)
    else:
        line = ("    "*spaces) + str(current_node) + "\n"
        file_tree.write(line)

parser = yacc.yacc(debug=True)
entrada = Path("entrada.txt").read_text()
parserOut = parser.parse(entrada)
file_tree = open("tree.txt", "w+")
build_tree(parserOut)
file_tree.close()
analizador_semantico = AnalizadorSemantico()
analizador_semantico.preenche_SymbolTable_e_Verifica(parserOut)
codeGenerator(parserOut)