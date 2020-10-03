# Declaracion de variables
# En la linea 240 aproximadamente hay un "main" donde esta el archivo que leera el programa

operaciones = ["MOV", "ADD", "SUB", "AND", "OR", "NOT", "XOR", "SHL", "SHR", "INC", "RST", "CMP", "JMP", "JEQ", "JNE",
               "JGT", "JLT", "JGE", "JLE", "JCR", "JOV"]

"""
INC,RST,JMP
MOV
ADD,SUB,AND,OR,XOR
NOT,SHL,SHR
CMP
"""

"""
Funciones auxiliares
"""

def safe_int_cast(val):
    try:
        val = int(val)
    except (ValueError, TypeError):
        return False
    return True


def hex_to_dec(string):
    string = string.replace("#", "")
    return int(string, 16)

def par_removal(string):
    string = string.replace("(", "")
    string = string.replace(")", "")
    return string

def par_adder(string):
    return "("+str(string)+")"

def cleaner(linea):
    if "(" in linea:
        linea = par_removal(linea)
        if "#" in linea:
            linea = hex_to_dec(linea)
        linea = par_adder(linea)
    if "#" in linea:
        linea = hex_to_dec(linea)
        linea = str(linea)

    return linea



def p_checker(string):
    if string == "(B)":
        return True
    if string[0] == "(" and string[-1] == ")":
        string = par_removal(string)
        print (string)
        if "#" in string:
            string = str(hex_to_dec(string))
        checker = safe_int_cast(string)
        if checker:
            string = par_adder(string)
            print (string)
            return True
    return False


"""
Funciones reales
"""


def unique_checker(insert, largo):  # INC, RST , JMP
    verificador = False

    if type(insert[1])!=list:
        if "A" in insert[1] or (insert[1]=="(B)" and "J" in insert[0]):  # Revisor A no puede existir en instrucciones unicas
            return 2
        if "#" in insert[1]:
            insert[1] = str(hex_to_dec(insert[1]))

        if insert[1]!="(B)":
            if "(" in insert[1]:
                insert[1]=par_removal(insert[1])
                verificador = True
            if int(insert[1]) > largo and "J" in insert[0]:  # A futuro va a ser el label no existente

                if verificador:
                    insert[1]=par_adder(insert[1])
                return 3
            if int(insert[1]) > 255 and insert[1]!="B":  # Revisor Jump < largo de instrucciones o Lit<255

                if verificador:
                    insert[1]=par_adder(insert[1])
                return 1

            if verificador:
                insert[1]=par_adder(insert[1])
            return 0

    elif type(insert)==list:
        return 2

    return 0


def mov_checker(insert):
    if type(insert[1]) == list:
        if insert[1][1] == insert[1][0]:
            return 2  # => Instruccion no valida

        if p_checker(insert[1][0]) and not (insert[1][1] == "A" or insert[1][1] == "B"):
            return 2  # => Instruccion no valida

        if "(B)" == insert[1][0] and not insert[1][1]=="A":
            return 2 #=> si es B, solo puede haber A a la derecha
        return 0
    return 2


def add_sub_and_or_xor_checker(insert):
    if type(insert[1]) == list:
        if insert[1][1] == insert[1][0]:
            return 2  # => Instruccion no valida
        if insert[1][0] == "B" and insert[1][1] == "(B)":
            return 2  # => Instruccion no valida
        if p_checker(insert[1][0]):
            return 2
        if insert[1][0] == "(B)":
            return 2
    else:
        if not p_checker(insert[1]) or insert[1] == "(B)":
            return 2
    return 0


def not_shl_shr(insert):
    if insert[1] == "(B)":
        return 0
    if type(insert[1]) == list:
        if (insert[1][0] == "A" or insert[1][0] == "B") and (insert[1][1] == "A" or insert[1][1] == "B"):
            return 0
        if p_checker(insert[1][0]) and (insert[1][1] == "A" or insert[1][1] == "B"):
            return 0
    return 2


def cmp(insert):
    if type(insert[1]) == list:
        if insert[1][0] == insert[1][1]:
            return 2
        if insert[1][0] == "A":
            return 0
        if insert[1][0] == "B" and ((p_checker(insert[1][1]) or insert[1][1] != "A") and insert[1][1] != "(B)"):
            return 0
    return 2


def lit(insert):
    if insert[1][1] != "A" and insert[1][1] != "B" and p_checker(insert[1][1]):
        if insert[1][1] == "(B)":
            return 0

        string = insert[1][1].replace("(", "")
        string = string.replace(")", "")

        if int(string) > 255:
            return 1  # Instruccion fuera de rango

    elif insert[1][1] != "A" and insert[1][1] != "B" and not p_checker(insert[1][1]):
        if int(insert[1][1]) > 255:
            return 1  # Instruccion fuera de rango

    if insert[1][0] != "A" and insert[1][0] != "B" and p_checker(insert[1][0]):
        if insert[1][0] == "(B)":
            return 0

        string = insert[1][0].replace("(", "")
        string = string.replace(")", "")
        if int(string) > 255:
            return 1  # Instruccion fuera de rango

    elif insert[1][0] == "A" or insert[1][0] == "B":
        return 0

    return 2


def revisar_instruccion(insert, largo):
    if insert[0] in operaciones:
        if type(insert[1]) == list:
            if "(A)" in insert[1][0] or "(A)" in insert[1][1]:
                return f"para la instruccion {insert[0]} no existe el uso con {insert[1]}"

            if insert[1][0] != "A" and insert[1][0] != "B" and not p_checker(insert[1][0]):
                return f"para la instruccion {insert[0]} no existe el uso con {insert[1]}"  # => Literal en la izquierda

        if "J" in insert[0] or insert[0] == "INC" or insert[0] == "RST":
            #  primera revision
            checker = unique_checker(insert, largo)
            if checker == 1:
                return "instruccion fuera de rango permitido"  # Lit>255

            elif checker == 2 or "(A)" in insert[1]:
                return f"para la instruccion {insert[0]} no existe el uso con {insert[1]}"  # No puede haber A en instrucciones unicas

            elif checker == 3:
                return "JMP a instruccion inexistente"  # Cambiar por label a futuro

        else:
            if "(A)" in insert[1]:
                return f"para la instruccion {insert[0]} no existe el uso con {insert[1]}"

            #  segunda revision
            if insert[0] == "MOV":
                checker = mov_checker(insert)
                if checker == 2:
                    return f"para la instruccion {insert[0]} no existe el uso con {insert[1]}"  # Instruccion invalida

            # tercera revision
            elif insert[0] == "ADD" or insert[0] == "SUB" or insert[0] == "AND" or insert[0] == "OR" or \
                    insert[0] == "XOR":
                checker = add_sub_and_or_xor_checker(insert)
                if checker == 2:
                    return f"para la instruccion {insert[0]} no existe el uso con {insert[1]}"

            # cuarta revision
            elif insert[0] == "NOT" or insert[0] == "SHL" or insert[0] == "SHR":
                checker = not_shl_shr(insert)

                if checker == 2:
                    return f"para la instruccion {insert[0]} no existe el uso con {insert[1]}"

            # quinta revision
            else:
                checker = cmp(insert)
                if checker == 2:
                    return f"para la instruccion {insert[0]} no existe el uso con {insert[1]}"

            # Revision de rango
            checker = lit(insert)
            if checker == 1:
                return "se usa literal fuera de rango permitido"

        return True

    return f"la instruccion no existe {insert[0]}"


def leer_archivo(nombre):
    file = open(nombre)
    inst = []
    for linea in file:
        linea = linea.split()
        if "," in linea[1]:
            linea[1] = linea[1].split(",")
            linea[1][0] = cleaner(linea[1][0])
            linea[1][1] = cleaner(linea[1][1])
        else:
            linea[1] = cleaner(linea[1])
        inst.append(linea)
    return inst

def revisor(archivo):
    instrucciones = leer_archivo(archivo)
    cont = 1
    verificador = True
    for ins in instrucciones:
        tmp = revisar_instruccion(ins, len(instrucciones))
        if tmp != True:
            print(f"Error en la linea {cont} {tmp}")
            verificador = False
        cont += 1
    if verificador:
        print (f"Lineas de codigo del archivo original: {cont-1}")
    return instrucciones,verificador

"""
OP CODES PROCESSING
"""
def opcodes(operaciones):
    dic = {}
    cont = 0
    aux = ""
    stringaux = ""
    check = True
    archivo = open("test.txt")
    for linea in archivo:
        if linea=="\n":
            check = True
            continue

        linea = linea.replace("\n","")

        if linea in operaciones and check:
            aux = linea
            check = False
            continue

        cont+=1
        if cont==1:
            stringaux=aux+" "+linea

        if cont==2:
            dic[stringaux]=linea
            stringaux=""
            cont = 0
    return dic

def num_or_dir(ins,jumper):

    if ins!="A" and ins!="B" and ins!="(B)":

        if jumper:
                aux = int(ins)
                ins = "Dir"
                return aux,ins
        else:
            if "(" in ins:
                aux = par_removal(ins)
                aux = int(aux)
                ins = "(Dir)"
                return aux,ins
            else:
                aux = int(ins)
                ins = "Lit"
                return aux,ins
    return 0,ins


# Main

archivo = "p3_1-correccion1.ass"
instrucciones,verificador = revisor(archivo)
if verificador:
    dic = opcodes(operaciones)
    out = open("file.out","w")
    for ins in instrucciones:
        if type(ins[1])==list:
            num,ins[1][0] = num_or_dir(ins[1][0],False)
            if num==0:
                num,ins[1][1]= num_or_dir(ins[1][1],False)
            string = ins[0]+" "+ins[1][0]+","+ins[1][1]
        else:
            if "J" in ins[0]:
                num,ins[1] = num_or_dir(ins[1],True)
            else:
                num,ins[1] = num_or_dir(ins[1],False)
            string = ins[0]+" "+ins[1]
        print (string)
        out.write(dic[string]+format(num,"08b")+"\n")



out.close()