from SymbolTable import SymbolTable
from Symbol import Symbol

class AnalizadorSemantico(object):
    def __init__(self):
        self.qtdTabelas = 1
        self.symtab = []
        self.symtab.append(SymbolTable())
        self.qtdClasses = 0
        self.declClasses = SymbolTable()
        self.qtd_true_branch = 0
        self.qtd_false_branch = 0
        self.qtd_endif_branch = 0
        self.qtdWhile = 0
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

    def validate_class(self, key, expected_value, current_value , scope):
        array_Decl = self.declClasses.find(key)
        if current_value in array_Decl:
            if current_value == expected_value:
                if scope <= array_Decl[1]:
                    return True
        return False

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
            #FAZ COISAS
            self.counter_scope -= 1
        
        if(cmd.leaf[0] == "if"):
            if(contain_leaf(cmd, "else")):
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
            cmd_id = cmd.children[0]
            if (cmd_id.leaf[0] == "="):
                validate_class()

    def resolve_exp(self,exp):
        pass

    def preenche_SymbolTable(self, prog):
        #'prog : main classes'
        main = self.achar_Filhos(prog, "main")
        classes = self.achar_Filhos(prog, "classes")

        if (main is not None):
            #'main : CLASS ID ECHAVE PUBLIC STATIC VOID MAIN 
            #            EPARENTESE STRING ECOLCHETE DCOLCHETE ID 
            #               DPARENTESE ECHAVE cmd DCHAVE DCHAVE'
            #
            self.qtdClasses += 1
            self.counter_scope += 1
            self.declClasses.insert(main.leaf[1],main.leaf[0], self.counter_scope) 
        

        main_cmd = self.achar_Filhos(main, "cmd")

        self.resolve_cmd(main_cmd)

        if (classes is not None):
            # print(classes.type)
            # print(classes.leaf)
            pass

        print(self.validate_class('Factorial', 'class', 'class', 1))    
        print(self.declClasses)


