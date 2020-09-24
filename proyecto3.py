# Declaracion de variables
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
        return True
    except (ValueError, TypeError):
        return False


def hex_to_dec(string):
    return int(string, 16)


def p_checker(string):
    if string == "(B)":
        return True
    if string[0] == "(" and string[-1] == ")":
        aux = string
        aux = string.replace("(", "")
        aux = aux.replace(")", "")
        if "#" in string:
            aux = aux.replace("#", "")
            aux = str(hex_to_dec(aux))
        checker = safe_int_cast(aux)
        if checker:
            string = "(" + aux + ")"
            return True
    return False


"""
Funciones reales
"""


def unique_checker(insert, largo):  # INC, RST , JMP
    if "J" in insert[0] or insert[0] == "INC" or insert[0] == "RST":
        if "A" in insert[1]:  # Revisor A no puede existir en instrucciones unicas
            return 2  # => Instruccion no valida
        if "#" in insert[1]:
            insert[1] = insert[1].replace("#", "")
            insert[1] = str(hex_to_dec(insert[1]))

        if (int(insert[1]) > largo and "J" in insert[0]) or int(
                insert[1]) > 255:  # Revisor Jump < largo de instrucciones o Lit<255
            return 1  # => "Instruccion fuera de rango permitido"

    return 0  # todo correcto xdxd


def mov_checker(insert):
    if insert[1][1] == insert[1][0]:
        return 2  # => Instruccion no valida
    if p_checker(insert[1][0]) and not (insert[1][1] == "A" or insert[1][1] == "B"):
        return 2  # => Instruccion no valida
    return 0  # todo correcto xdxd


def add_sub_and_or_xor_checker(insert):
    if insert[1][1] == insert[1][0]:
        return 2  # => Instruccion no valida
    if insert[1][0] == "B" and insert[1][1] == "(B)":
        return 2  # => Instruccion no valida
    if type(insert[1]) == list:
        if p_checker([1][0]):
            return 2  # => Instruccion no valida
    if insert[1][0] == "(B)":
        return 2  # => Instruccion no valida
    return 0  # todo correcto xdxd


def revisar_instruccion(insert, largo):
    if insert[0] in operaciones:
        #  primera revision
        checker = unique_checker(insert, largo)
        if checker == 1:
            return "Instruccion fuera de rango permitido"
        elif checker == 2 or "(A)" in insert[1]:
            return "Instruccion no valida"

        if type(insert[1]) == list:
            if insert[1][0] != "A" and insert[1][0] != "B" and not p_checker(insert[1][0]):
                return 2  # => Instruccion no valida
        #  segunda revision
        checker = mov_checker(insert)
        if checker == 2:
            return "Instruccion no valida"

        # tercera revision
        if checker == 2:
            return "Instruccion no valida"

        return True
    return "La Instruccion no existe"


def leer_archivo(nombre):
    file = open(nombre)
    inst = []
    for linea in file:
        linea = linea.split()
        inst.append(linea)
    for op in inst:
        if "," in op[1]:
            op[1] = op[1].split(",")
    return inst


# Main

archivo = "input.txt"
instrucciones = leer_archivo(archivo)
for ins in instrucciones:
    tmp = revisar_instruccion(ins, len(instrucciones))
    if not tmp:
        print(tmp, ins)
