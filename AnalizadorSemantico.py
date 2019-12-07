from SymbolTable import SymbolTable

class AnalizadorSemantico(object):
    def __init__(self):
        self.TabelaSimbolos = SymbolTable()
        self.counter_scope = 0

    def achar_Filhos(self, Node, tipo):
        for child in Node.children:
            if(child.type == tipo):
                return child
        return None

    def contain_leaf(self, Node, leaf):
        for current_leaf in Node.leaf:
            if(current_leaf == leaf):
                return True
        return False

    def validate_key(self, key,scope, expected_value = None):
        array_Decl = self.TabelaSimbolos.find(key)
        if array_Decl is not None:
            current_value = array_Decl[0]
            if current_value == expected_value or expected_value is None:
                if(self.counter_scope > 0):
                    if(array_Decl[1] == "params"):
                        return True
                    if scope >= array_Decl[1]:
                        return True
                else:
                    if(array_Decl[1] == "params"):
                        return True
                    if scope <= array_Decl[1]:
                        return True 
        raise Exception (
            'Simbolo ' + key + ' não declarado no escopo'
        )

    def validate_type(self, type1, type2):
        if (type1 != type2):
            raise Exception (
                'Erro de operacao entre tipos de variavel'
            )
        return True

    def resolve_cmd(self,cmd):
        # cmd :     ECHAVE cmds DCHAVE
        #     | IF EPARENTESE exp DPARENTESE cmd ELSE cmd
        #     | IF EPARENTESE exp DPARENTESE cmd
        #     | WHILE EPARENTESE exp DPARENTESE cmd
        #     | PRINT EPARENTESE exp DPARENTESE SEMICOLON
        #     | ID cmd_id
        if(cmd.leaf[0] == "{"):
            self.counter_scope += 1
            cmd_cmds = self.achar_Filhos(cmd, "cmds")
            self.resolve_cmds(cmd_cmds)
            self.counter_scope -= 1
        
        if(cmd.leaf[0] == "if"):
            if(self.contain_leaf(cmd, "else")):
                cmd_exp = self.achar_Filhos(cmd, "exp")
                cmd_cmd1 = self.achar_Filhos(cmd, "cmd")
                cmd_cmd2 = cmd.children[len(cmd.children) - 1]
                self.resolve_exp(cmd_exp)
                self.resolve_cmd(cmd_cmd1) 
                self.resolve_cmd(cmd_cmd2) 
            else:
                cmd_exp = self.achar_Filhos(cmd, "exp")
                cmd_cmd1 = self.achar_Filhos(cmd, "cmd")
                self.resolve_exp(cmd_exp)
                self.resolve_cmd(cmd_cmd1)

        if(cmd.leaf[0] == "while"):
            cmd_exp = self.achar_Filhos(cmd, "exp")
            cmd_cmd = self.achar_Filhos(cmd, "cmd")
            self.resolve_exp(cmd_exp)
            self.resolve_cmd(cmd_cmd)

        if(cmd.leaf[0].lower() == "system.out.println"):
            cmd_exp = self.achar_Filhos(cmd, "exp")
            self.resolve_exp(cmd_exp)

        if(cmd.children[0].type == "cmd_id"):
            #cmd_id :   OP_ASSIGN exp SEMICOLON
            #         | ECOLCHETE exp DCOLCHETE OP_ASSIGN exp SEMICOLON
            self.validate_key(cmd.leaf[0], self.counter_scope)
            cmd_id = cmd.children[0]
            if (cmd_id.leaf[0] == "="):
                cmd_id_exp = self.achar_Filhos(cmd_id, "exp")
                self.resolve_exp(cmd_id_exp)

                self.validate_type(self.get_type(cmd.leaf[0]),self.get_exp_type(cmd_id_exp))

            if (cmd_id.leaf[0] == "["):
                cmd_id_exp1 = cmd_id.children[0]
                cmd_id_exp2 = cmd_id.children[1]
                self.resolve_exp(cmd_id_exp1)
                self.resolve_exp(cmd_id_exp2)

        
    def get_type(self, key):
        return self.TabelaSimbolos.find(key)[0]        

    def get_exp_type(self, exp):
        if(len(exp.leaf) > 0):
            # exp : exp OP_AND rexp
            return "boolean"
        else:
            rexp = self.achar_Filhos(exp, "rexp")
            if(rexp is not None):
                return self.get_rexp_type(rexp)

    def get_rexp_type(self, rexp):
        #rexp : rexp rexp2
        #    | aexp
        # Caso rexp2 que envolve apenas operadores os logicos (<, ==, !=) temos booleanos
        if(len(rexp.children) > 1):
            return "boolean"
        else:
             return self.get_aexp_type(self.achar_Filhos(rexp, "aexp"))

    def get_aexp_type(self,aexp):
        #aexp : aexp OP_MAIS mexp
        #    | aexp OP_MENOS mexp
        #    | mexp
        if(len(aexp.leaf) > 0):
            aexp_aexp = self.achar_Filhos(aexp, "aexp")
            aexp_mexp = self.achar_Filhos(aexp, "mexp")
            #Operacoes entre exp devem ser checadas se são validas
            self.validate_type(self.get_exp_type(aexp_aexp), self.get_mexp_type(aexp_mexp))
            # Como a gramática só tem tipo inteiro nesses casos podemos retornar int
            return "int"
        else:
            aexp_mexp = self.achar_Filhos(aexp, "mexp")
            return self.get_mexp_type(aexp_mexp)



    def get_mexp_type(self, mexp):
        #mexp : mexp OP_MULTIPLICA sexp
        #    | sexp
        if(len(mexp.leaf) > 0):
            mexp_mexp = self.achar_Filhos(mexp, "mexp")
            mexp_sexp = self.achar_Filhos(mexp, "sexp")
            #Operacoes entre exp devem ser checadas se são validas
            self.validate_type(self.get_mexp_type(mexp_mexp), self.get_sexp_type(mexp_sexp))
            # Como a gramática só tem tipo inteiro nesses casos podemos retornar int
            return "int"
        else:
            mexp_sexp = self.achar_Filhos(mexp, "sexp") 
            return self.get_sexp_type(mexp_sexp)

    def get_sexp_type(self, sexp):
        #sexp :    OP_NAO sexp << boolean
        #    | OP_MENOS sexp << int
        #    | TRUE << boolean
        #    | FALSE << boolean
        #    | NUMBER << int
        #    | NULL << Apenas em RunTime
        #    | NEW INT ECOLCHETE exp DCOLCHETE << int[]
        #    | pexp PONTO LENGTH << int
        #    | pexp ECOLCHETE exp DCOLCHETE
        #    | pexp
        if(len(sexp.leaf) > 0):
            if(sexp.leaf[0] == "!"):
                return "boolean"
            elif(sexp.leaf[0] == "-"):
                return "int"
            elif(len(sexp.children) == 0):
                return "int"
            elif(sexp.leaf[0] == "new"):
                return "int[]"
            elif(sexp.leaf[0] == "."):
                return "int"
            elif(sexp.leaf[0].lower() == "true"):
                return "boolean"
            elif(sexp.leaf[0].lower() == "false"):
                return "boolean"
            else:
                sexp_pexp = self.achar_Filhos(sexp, "pexp")
                if(sexp_pexp is not None):
                    return self.get_pexp_type(sexp.children[0])
                else:
                    raise Exception(
                        'Não foi possivel verificar o tipo da variavel'
                    )
    
    def get_pexp_type(self, pexp):
        #pexp :    ID << class  X
        #    | THIS << class X
        #    | NEW ID EPARENTESE DPARENTESE << class X
        #    | EPARENTESE exp DPARENTESE << exp type
        #    | pexp PONTO ID << String
        #    | pexp PONTO ID EPARENTESE exps DPARENTESE << expsType
        #    | pexp PONTO ID EPARENTESE DPARENTESE << class
        if(len(pexp.children) == 0):
            return "class"
        else:
            if(pexp.leaf[0] == "("):
                pexp_exp = self.achar_Filhos(pexp, "exp")
                return self.get_exp_type(pexp_exp)
            elif(len(pexp.leaf) == 2):
                return "String"
            else:
                pexp_exps = self.achar_Filhos(pexp, "exps")
                if(pexp_exps is not None):
                    return self.get_exps_type(pexp_exps)
                else:
                    return "class"

    def get_exps_type(self, exps):
        #'exps : exp sequenciaexp'
        #sequenciaexp : VIRGULA exp sequenciaexp
        #                | empty
        return self.get_exp_type(exps.children[0])


    def resolve_exp(self,exp):
        #exp : exp OP_AND rexp
        #    | rexp
        if (len(exp.leaf) > 0):
            if(exp.leaf[0] == "="):
                self.resolve_exp(exp.children[0])
                self.resolve_rexp(exp.children[1])
        else:
            self.resolve_rexp(exp.children[0])
            
    def resolve_rexp(self,rexp):        
        #rexp : rexp rexp2
        #    | aexp
        if (len(rexp.children) > 1):
            self.resolve_rexp(rexp.children[0])
            self.resolve_rexp2(rexp.children[1])
        else:
            self.resolve_aexp(rexp.children[0])

    def resolve_rexp2(self, rexp2):
        #rexp2 : OP_MENOR aexp
        #       | OP_IGUAL aexp
        #       | OP_NAO_IGUAL aexp
        self.resolve_aexp(rexp2.children[0])

    

    def  resolve_aexp(self, aexp):
        #aexp : aexp OP_MAIS mexp
        #    | aexp OP_MENOS mexp
        #    | mexp
        if(len(aexp.leaf) > 0):
            self.resolve_aexp(aexp.children[0])
            self.resolve_mexp(aexp.children[1])
        else:
            self.resolve_mexp(aexp.children[0])

    def resolve_mexp(self, mexp):
        #mexp : mexp OP_MULTIPLICA sexp
        #    | sexp
        if (len(mexp.leaf) > 0):
            self.resolve_mexp(mexp.children[0])
            self.resolve_sexp(mexp.children[1])
        else:
            self.resolve_sexp(mexp.children[0])

    def resolve_sexp(self, sexp):
        #sexp :    OP_NAO sexp
        #    | OP_MENOS sexp
        #    | TRUE
        #    | FALSE
        #    | NUMBER
        #    | NULL
        #    | NEW INT ECOLCHETE exp DCOLCHETE
        #    | pexp PONTO LENGTH
        #    | pexp ECOLCHETE exp DCOLCHETE
        #    | pexp
        if(len(sexp.leaf) > 0):
            if(sexp.leaf[0] == "!"):
                self.resolve_sexp(sexp.children[0])
            if(sexp.leaf[0] == "-"):
                self.resolve_sexp(sexp.children[0])
        else:
            self.resolve_pexp(sexp.children[0])

    def resolve_pexp(self, pexp):
        #pexp :    ID
        #    | THIS
        #    | NEW ID EPARENTESE DPARENTESE
        #    | EPARENTESE exp DPARENTESE
        #    | pexp PONTO ID
        #    | pexp PONTO ID EPARENTESE exps DPARENTESE
        #    | pexp PONTO ID EPARENTESE DPARENTESE
        pass

    def resolve_classes(self, classes):
        if (classes.children[0].type != "empty"):
            self.resolve_classes(classes.children[0])
            self.resolve_classe(classes.children[1])


    def resolve_classe(self, classe):
        # classe : CLASS ID extends_id ECHAVE variaveis metodos DCHAVE
        self.TabelaSimbolos.insert(classe.leaf[1], "class", self.counter_scope)
        variaveis = self.achar_Filhos(classe, "variaveis")
        self.resolve_variaveis(variaveis)
        metodos = self.achar_Filhos(classe, "metodos")
        self.resolve_metodos(metodos)

    def pop_all_params(self):
        for k,v in list(self.TabelaSimbolos._symbols.items()):
            if "params" in v:
                print('\n Remove all function params in scope')
                del self.TabelaSimbolos._symbols[k]

    def resolve_metodos(self, metodos):
        
        #metodos : metodos metodo 
        #    | empty
        if (metodos.children[0].type != "empty"):
            self.resolve_metodos(metodos.children[0])
            #metodo : PUBLIC tipo ID EPARENTESE params_o DPARENTESE 
            #            ECHAVE variaveis cmds RETURN exp SEMICOLON DCHAVE
            metodo = self.achar_Filhos(metodos, "metodo")
            if(self.counter_scope > 0):
                self.counter_scope += 1
            else:
                self.counter_scope -= 1
            self.TabelaSimbolos.insert(metodo.leaf[1], "class", self.counter_scope)

            #params : tipo ID sequenciaparams
            params = self.achar_Filhos(self.achar_Filhos(metodo, "params_o"), "params")
            if params is not None:
                self.resolve_params(params)

            variaveis = self.achar_Filhos(metodo, "variaveis")
            self.resolve_variaveis(variaveis)
            
            print(self.TabelaSimbolos)

            cmds = self.achar_Filhos(metodo,"cmds")

            self.resolve_cmds(cmds)

            exp = self.achar_Filhos(metodo, "exp")

            self.resolve_exp(exp)

            # Acabou a funcao deleta parametros do escopo e muda o escopo
            if(self.counter_scope > 0):
                self.counter_scope -= 1
            else:
                self.counter_scope += 1 
            self.pop_all_params()
            
    def resolve_cmds(self, cmds):
        #cmds : cmd cmds
        #    | empty
        if(len(cmds.children) > 1):
            cmds_cmd = self.achar_Filhos(cmds, "cmd")
            cmds_cmds = self.achar_Filhos(cmds, "cmds")
            self.resolve_cmd(cmds_cmd)
            self.resolve_cmds(cmds_cmds)
        else:
            pass


    def resolve_params(self,params):
        tipo = self.achar_Filhos(params, "tipo")
        self.TabelaSimbolos.insert(params.leaf[0], self.procura_tipo(tipo), "params")

        sequenciaparams = self.achar_Filhos(params, "sequenciaparams")
        self.resolve_sequencia_params(sequenciaparams)

    def resolve_sequencia_params(self, sequenciaparams):
        #sequenciaparams : SEMICOLON tipo ID sequenciaparams
        #            | empty
        tipo = self.achar_Filhos(sequenciaparams, "tipo")
        if (tipo is not None):
            self.TabelaSimbolos.insert(sequenciaparams.leaf[1], self.procura_tipo(tipo), "params")
            self.resolve_sequencia_params(self.achar_Filhos(sequenciaparams, "sequenciaparams"))

    def procura_tipo(self, classe_tipo):
        if (len(classe_tipo.children) > 0):
            tipo2 = classe_tipo.children[0]
            if(len(tipo2.children) > 0):
                return "int"
            else:
                return "int[]"
        else:
            return classe_tipo.leaf[0]


    def resolve_variaveis(self, variaveis):
        # variaveis : variaveis variavel
        #      | empty    

        # variavel : tipo ID SEMICOLON
        if (variaveis.children[0].type != "empty"):
            self.resolve_variaveis(variaveis.children[0])
            variavel = self.achar_Filhos(variaveis, "variavel")
            tipo_variavel = variavel.children[0]
            if(len(tipo_variavel.children) > 0):
                tipo2 = tipo_variavel.children[0]
                if(len(tipo2.children) > 0):
                    self.TabelaSimbolos.insert(variavel.leaf[0], "int", self.counter_scope)
                else:
                    self.TabelaSimbolos.insert(variavel.leaf[0], "int[]", self.counter_scope)
            else:
                if(tipo_variavel.leaf[0] == "boolean"):
                    self.TabelaSimbolos.insert(variavel.leaf[0], "boolean", self.counter_scope)
                else:
                    self.TabelaSimbolos.insert(variavel.leaf[0], "class", self.counter_scope)

        

    def preenche_SymbolTable(self, prog):
        #'prog : main classes'
        main = self.achar_Filhos(prog, "main")
        classes = self.achar_Filhos(prog, "classes")

        if (main is not None):
            #'main : CLASS ID ECHAVE PUBLIC STATIC VOID MAIN 
            #            EPARENTESE STRING ECOLCHETE DCOLCHETE ID 
            #               DPARENTESE ECHAVE cmd DCHAVE DCHAVE'
            #
            self.counter_scope += 1
            self.TabelaSimbolos.insert(main.leaf[1],main.leaf[0], self.counter_scope) 
            self.TabelaSimbolos.insert("main", "static void", self.counter_scope)

        main_cmd = self.achar_Filhos(main, "cmd")

        self.resolve_cmd(main_cmd)

        #FLIPA PARA NEGATIVO OS ESCOPOS PARA DEFINIR QUE TEM MAIS DE UMA CLASSE NO ARQUIVO
        self.counter_scope *= -1

        if (classes is not None):
            self.resolve_classes(classes)

        print(self.validate_key('Factorial', 1))    
        print(self.TabelaSimbolos)
    
