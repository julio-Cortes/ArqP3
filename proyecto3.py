###Declaracion de variables ###
instrucciones = ["MOV","ADD","SUB", "AND","OR","NOT","XOR","SHL","SHR","INC","RST","CMP","JMP","JEQ","JNE",
                 "JGT","JLT","JGE","JLE","JCR","JOV"]

def revisar_instruccion(instrucciones,insert):
    if insert[0] in instrucciones:
        if
        if "J" in insert[0]:
            if "#" in insert[1]:
                insert[1]=insert[1].replace("#","")
                print(hex_to_dec(insert[1]))
        if "(A)" in insert[1]:
            return "Instruccion no valida"
        return True
    return "La Instruccion no existe"

def leer_archivo(nombre):
    file = open(nombre)
    operaciones=[]
    for linea in file:
        linea = linea.split()
        operaciones.append(linea)
    return operaciones

def hex_to_dec(string):
    return int(string,16)




###Main###
file = "p3-ej_incorrecto.ass"
operaciones=leer_archivo(file)
for ins in operaciones:
    (revisar_instruccion(instrucciones,ins))



