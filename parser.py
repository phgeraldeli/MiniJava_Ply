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
        'classe : CLASS ID EXTENDS ID ECHAVE variaveis metodos DCHAVE'
    

    #multiplas variáveis
    def p_variaveis(p):
        pass

    def p_variavel(p):
        pass

    def p_metodo(p):
        'metodo : PUBLIC tipo ID EPARENTESE '
        pass
    
    #multiplos métodos
    def p_metodos(p):
        pass