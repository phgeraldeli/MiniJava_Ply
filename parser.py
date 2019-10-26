import ply.yacc as yacc
from scanner import tokens

##########
# Parser para a linguagem mini-java
#########


if __name__ == "__main__":
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
        'classes : classe | classes classe'
        p[0] = ('classes',p[1:])

    def p_classe(p):
        '''
        classe : CLASS ID EXTENDS ID ECHAVE variaveis metodos DCHAVE 
        | CLASS ID ECHAVE variaveis metodos DCHAVE
        '''
        p[0] = ('classe', p[1:])    

    #multiplas variáveis
    def p_variaveis(p):
        'variaveis : variavel | variaveis variavel'
        p[0] = ('variaveis', p[1:])

    def p_variavel(p):
        'variavel : tipo ID SEMICOLON'
        p[0] = ('variavel', p[1:])

    #multiplos métodos
    def p_metodos(p):
        'metodos : metodo | metodos metodo'
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
                        | SEMICOLON tipo ID
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
        'cmds : cmd | cmds cmd'
        p[0] = ('cmds', p[1:])

    def p_cmd(p):
        '''
        'cmd : ECHAVE cmds DCHAVE
              | if EPARENTESE exp DPARENTESE cmd  
              | if EPARENTESE exp DPARENTESE cmd ELSE cmd
              | WHILE EPARENTESE exp DPARENTESE cmd
              | PRINT ECHAVE exp DCHAVE
              | ID OP_ASSIGN exp 
              | ID ECOLCHETE exp DCOLCHETE OP_ASSIGN exp
        ''' 
        p[0] = ('cmd', p[1:])