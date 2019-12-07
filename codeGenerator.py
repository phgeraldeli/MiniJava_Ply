beq_counter = 0

def codeGenerator(entrada):
    with open('out.txt', 'w') as out:
        string = cgen(entrada)
        out.write(string)

def cgen(entrada):
    # print(entrada.children[1].type)
    if(entrada.children[0] is not None):
        parte1 = cgenMain(entrada.children[0])
    if(entrada.children[1] is not None):
        parte2 = cgen_Multiplas_Classes(entrada.children[1])
    string = f"{parte1}\n{parte2}"
    return string

def cgen_Multiplas_Classes(entrada):
    string = ""
    if(len(entrada.children) > 1):
        string += cgen_classe(entrada.children[1])
        string += cgen_Multiplas_Classes(entrada.children[0])
    return string

def cgen_classe(entrada):
    string = ""
    if (len(entrada.children) > 1):
        string = cgen_multiplas_variaveis(entrada.children[1])
        string += cgen_multiplos_metodos(entrada.children[2])
    return string

def cgen_multiplos_metodos(entrada):
    string = ""
    if ( len(entrada.children) > 1):
        string += cgen_public(entrada)
        string += cgen_multiplos_metodos(entrada.children[1])
    return string

def cgen_public(entrada):
    string = ""
    for child in entrada.children:
        if(child.type == "cmds"):
            string += cgen_multiplas_cmds(child)
        if(child.type == "exp"):
            string += cgen_exp(child)
    return string

def cgen_multiplas_variaveis(entrada):
    string = ""
    if(len(entrada.children) > 1):
        string += cgen_tipo(entrada.children[0])
        string += cgen_multiplas_variaveis(entrada.children[1])
    return string

def cgen_tipo(entrada):
    return ""

def cgen_multiplas_cmds(entrada):
    string = ""

    if (len(entrada.children) > 1):
        string += cgenCMD(entrada.children[0])
        string += cgen_multiplas_cmds(entrada.children[1])
    return string

def cgenMain(entrada):
    parte1 = ""
    if(entrada.children[0] is not None):
        parte1 += cgenCMD(entrada.children[0])

    string = (
        f"move $fp $sp\n"
        f"sw $ra 0($sp)\n"
        f"addiu $sp $sp -4\n"
        f"{parte1}\n"
        f"lw $ra 4($sp)\n"
        f"addiu $sp $sp 4\n"
        f"lw $fp 0($sp)\n"
        f"jr $ra"
    )

    return string

def cgenCMD(entrada):
    parte1 = ""
    if (len(entrada.leaf) > 0):
        if(entrada.leaf[0] == "{"):
            parte1 += cgen_chave(entrada)
        elif(entrada.leaf[0].lower() == "if"):
            parte1 += cgen_if(entrada)
        elif(entrada.leaf[0].lower() == "else"):
            parte1 += cgen_elseif(entrada)
        elif(entrada.leaf[0].lower() == "while"):
            parte1 += cgen_while(entrada)
        elif(entrada.leaf[0].lower() == "system.out.println"):
            parte1 += cgen_sout(entrada)
    elif( len(entrada.leaf) > 1):
        if(entrada.leaf[1].lower() == "="):
            parte1 += cgen_assign(entrada)
        elif(entrada.leaf[1].lower() == "["):
            parte1 += cgen_id(entrada)
    return parte1

def cgen_chave(entrada):
    return cgen_multiplas_cmds(entrada.children[0])

def cgen_id(entrada):
    return ""

def cgen_assign(entrada):
    var = entrada.leaf[0]
    parte1 = cgen_exp(entrada.children[0])
    string = (
        f"{parte1}\n"
        f"la $t1 {var}\n"
        f"sw $a0 0($t1)"
    )
    return string

def cgen_sout(entrada):
    return (
        f"li $v0, 1\n"
        f"move $a0, $t0\n"
        f"syscall"
    )

def cgen_while(entrada):
    condicao = cgen_exp(entrada.children[0])
    parte1 = cgen_cmd(entrada.children[1])
    global beq_counter
    string += (
        f"{condicao}\n"
        f"sw $a0 0($sp)\n"
        f"addiu $sp $sp -4\n"
        f"start{beq_counter}:\n"
        f"beq $a0 $zero false{beq_counter}\n"
        f"{parte1}\n"
        f"b start{beq_counter}\n"
        f"false{beq_counter}:\n"
        f"addiu $sp $sp 4"
        )
    beq_counter += 1
    return string

def cgen_elseif(entrada):
    return ""

def cgen_if(entrada):

    cond = cgen_exp(entrada.children[0])
    parte1 = cgen_exp(entrada.children[1])

    global beq_counter
    string = (
        f"{cond}\n"
        f"sw $a0 0($sp)\n"
        f"addiu $sp $sp -4\n"
        f"beq $a0 $zero false{beq_counter}\n"
        f"{parte1}\n"
        f"false{beq_counter}:\n"
        f"addiu $sp $sp 4"
    )
    beq_counter += 1

    return string

def cgen_exp(entrada):
    string = ""
    if(len(entrada.children) > 0):
        string += cgen_exp_exp(entrada)
    else:
        string += cgen_exp_rexp(entrada)
    return string

def cgen_exp_exp(entrada):
    string = ""
    parte1 = ""
    parte2 = ""
    if(len(entrada.children) > 0):
        if(entrada.type == 'cmd'):
            parte1 += cgenCMD(entrada)
        else:
            parte1 += cgen_rexp(entrada.children[0])
    string += (
        f"{parte1}\n"
        f"sw $a0 0($sp)\n"
        f"addiu $sp $sp -4\n"
        f"lw $t1 4($sp)\n"
        f"and $a0 $t1 $a0\n"
        f"addiu $sp $sp 4"
    )
    return string

def cgen_rexp(entrada):
    # rexp : rexp rexp2
    #         | aexp
    string = ""
    if (len(entrada.children) > 1):
        string += cgen_rexp2(entrada)
    else:
        string += cgen_aexp(entrada.children[0])
    return string
    # if(len(entrada.children))

def cgen_rexp2(entrada):
    string = ""
    parte2 = ""
    parte1 = cgen_rexp(entrada.children[0])
    parte2 += cgen_aexp(entrada.children[1].children[0])
    global beq_counter
    if (entrada.children[1].leaf[0] == "<"):
        string += (
                f"{parte1}\n"
                f"sw $a0 0($sp)\n"
                f"addiu $sp $sp -4\n"
                f"{parte2}\n"
                f"lw $t1 4($sp)\n"
                f"slt $a0 $t1 $a0\n"
                f"addiu $sp $sp 4"
            )
    elif (entrada.children[1].leaf[0] == ">"):
        string += (
            f"{parte1}\n"
            f"sw $a0 0($sp)\n"
            f"addiu $sp $sp -4\n"
            f"{parte2}\n"
            f"lw $t1 4($sp)\n"
            f"slt $a0 $a0 $t1\n"
            f"addiu $sp $sp 4"
        )
    elif (entrada.children[1].leaf[0] == "=="):
        string += (
            f"{parte1}\n"
            f"sw $a0 0($sp)\n"
            f"addiu $sp $sp -4\n"
            f"{parte2}\n"
            f"lw $t1 4($sp)\n"
            f"beq $a0 $t1 true{beq_counter}\n"
            f"li $a0 0\n"
            f"b eo_true{beq_counter}\n"
            f"true{beq_counter}:\n"
            f"li $a0 1\n"
            f"eo_true{beq_counter}:\n"
            f"addiu $sp $sp 4"
        )
        beq_counter += 1
    elif (entrada.children[1].leaf[0] == "!="):
        string += (
                f"{parte1}\n"
                f"sw $a0 0($sp)\n"
                f"addiu $sp $sp -4\n"
                f"{parte2}\n"
                f"lw $t1 4($sp)\n"
                f"bne $a0 $t1 true{beq_counter}\n"
                f"li $a0 0\n"
                f"b eo_true{beq_counter}\n"
                f"true{beq_counter}:\n"
                f"li $a0 1\n"
                f"eo_true{beq_counter}:\n"
                f"addiu $sp $sp 4"
            )
        beq_counter += 1
    elif (entrada.children[1].leaf[0] == "<="):
        string += (
            f"{parte1}\n"
            f"sw $a0 0($sp)\n"
            f"addiu $sp $sp -4\n"
            f"{parte2}\n"
            f"lw $t1 4($sp)\n"
            f"slt $a0 $a0 $t1\n"
            f"beq $a0 $zero true{beq_counter}\n"
            f"li $a0 0\n"
            f"b eo_true{beq_counter}\n"
            f"true{beq_counter}:\n"
            f"li $a0 1\n"
            f"eo_true{beq_counter}:\n"
            f"addiu $sp $sp 4"
        )
        beq_counter += 1
    elif (entrada.children[1].leaf[0] == ">="):
        string += (
            f"{parte1}\n"
            f"sw $a0 0($sp)\n"
            f"addiu $sp $sp -4\n"
            f"{parte2}\n"
            f"lw $t1 4($sp)\n"
            f"slt $a0 $t1 $a0\n"
            f"beq $a0 $zero true{beq_counter}\n"
            f"li $a0 0\n"
            f"b eo_true{beq_counter}\n"
            f"true{beq_counter}:\n"
            f"li $a0 1\n"
            f"eo_true{beq_counter}:\n"
            f"addiu $sp $sp 4"
        )
        beq_counter += 1
    return string

def cgen_aexp(entrada):
    
    # aexp : aexp OP_MAIS mexp
    #         | aexp OP_MENOS mexp
    #         | mexp
    string = ""
    if (len(entrada.children) > 1):
        string += cgen_aexpRecursivo(entrada)
    else:
        string += cgen_mexp(entrada.children[0])
    return string

def cgen_aexpRecursivo(entrada):
    string = ""
    parte1 = cgen_aexp(entrada.children[0])
    parte2 = cgen_aexp(entrada.children[1])
    if (entrada.leaf[0] == "+"):
        string += (
            f"{parte1}\n"
            f"sw $a0 0($sp)\n"
            f"addiu $sp $sp -4\n"
            f"{parte2}\n"
            f"lw $t1 4($sp)\n"
            f"add $a0 $t1 $a0\n"
            f"addiu $sp $sp 4"
        )
    else:
        string += (
            f"{parte1}\n"
            f"sw $a0 0($sp)\n"
            f"addiu $sp $sp -4\n"
            f"{parte2}\n"
            f"lw $t1 4($sp)\n"
            f"sub $a0 $t1 $a0\n"
            f"addiu $sp $sp 4"
        )
    return string

def cgen_mexp(entrada):
    # '''
    # mexp : mexp OP_MULTIPLICA sexp
    #         | sexp
    # '''
    string = ""
    if (len(entrada.children) > 1):
        string += cgen_mexpRecursivo(entrada)
    else:
        string += cgen_sexp(entrada.children[0])
    
    return string

def cgen_mexpRecursivo(entrada):
    string = ""
    parte1 += cgen_mexp(entrada.children[0])
    parte2 += cgen_sexp(entrada.children[1])
    string += (
        f"{parte1}\n"
        f"sw $a0 0($sp)\n"
        f"addiu $sp $sp -4\n"
        f"{parte2}\n"
        f"lw $t1 4($sp)\n"
        f"mul $a0 $t1 $a0\n"
        f"addiu $sp $sp 4"
    )
    return string

def cgen_sexp(entrada):
    # sexp :    OP_NAO sexp
    #         | OP_MENOS sexp
    #         | TRUE
    #         | FALSE
    #         | NULL
    #         | NEW INT ECOLCHETE exp DCOLCHETE
    #         | pexp PONTO LENGTH
    #         | pexp ECOLCHETE exp DCOLCHETE
    #         | pexp
    #         | NUMBER
    string = ""
    if (len(entrada.children) > 0):
        if (entrada.children[0].type == "pexp"):
            string += cgen_pexp(entrada.children[0])
        else:
            if(entrada.leaf[0] == "!"):
                string += cgen_sexp_OPNAO(entrada)
            elif(entrada.leaf[0] == "-"):
                string += cgen_sexp_OPMINUS(entrada)
            elif(entrada.leaf[0] == "true"):
                string += "li $a0 0\n"
            elif(entrada.leaf[0] == "false"):
                string += "li $a0 0\n"
            elif(entrada.leaf[0] == "null"):
                string += "li $a0 0\n"
            elif(entrada.leaf[0] == "."):
                string += "li $a0 {entrada.children[0].leaf[0]}"
            elif(entrada.leaf[0] == "["):
                string += cgen_sexp_ECOLCHETE(entrada)
    else:
        string += cgen_sexp_number(entrada)
    return string

def cgen_sexp_OPNAO(entrada):
    parte1 = cgen_sexp(entrada.children[0])
    return (
        f"{parte1}\n"
        f"nor $a0 $a0 $zero"
    )

def cgen_sexp_OPMINUS(entrada):
    string = ""
    parte1 = self.cgen_sexp(entrada.children[0])
    string += (
        f"{parte1}\n"
        f"neg $a0 $a0"
    )
    return string

def cgen_sexp_ECOLCHETE(entrada):
    string = ""
    var = entrada.children[0].leaf[0]
    
    child = entrada.children[1]
    while True:
        child = child.children[0]
        if len(child.children[0]) < 1:
            break
    pos = 4 * int(child.leaf[0])
    string += (
        f"la $t1 {var}\n"
        f"lw $a0 {pos}($t1)"
    )
    return string
def cgen_sexp_number(entrada):
    string = ""
    num = int(entrada.leaf[0])
    string += (
        f"li $a0 {num}"
    )
    return string

def cgen_pexp(entrada):
    return (
        f"\nmove $fp 0(%sp)\n"
        f"sw $a0 0(%sp)\n"
        f"addiu $sp $sp -4\n"
        f"lw $t1 4($sp)\n"
        f"addiu $sp $sp 4"
    )
