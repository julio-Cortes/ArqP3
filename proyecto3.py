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

def hex_to_dec(string):
    if  "#" in string:
        string = string.replace("#", "")
        return int(string, 16)
    else:
        return int(string)

def par_removal(string):
    if "(" in string:
        string = string.replace("(", "")
        string = string.replace(")", "")
        return string,True
    else:
        return string,False

def par_adder(string):
    return "("+str(string)+")"


"""
Funciones reales
"""
def revisar_instruccion(ins,dic,largo):
    string  = ins[0]+" "
    if type(ins[1])==list:

        if ins[1][0]!="A" and ins[1][0]!="B" and ins[1][0]!="(B)" and ins[1][0]!="(A)":
            if "(" in ins[1][0]:
                ins[1][0],check=par_removal(ins[1][0])
                ins[1][0] = hex_to_dec(ins[1][0])
                if ins[1][0] > 255:
                    return f"Direccion fuera de rango permitido,{ins[1][0]}",-1
                if check:
                    ins[1][0]=par_adder(ins[1][0])
                string+="(Dir)"
            else:
                ins[1][0] = hex_to_dec(ins[1][0])
                if int(ins[1][0])>255:
                    return f"Literal fuera de rango permitido,{ins[1][0]}",-1
                string+="Lit"

        else:
            string +=ins[1][0]

        string+=","

        if ins[1][1]!="A" and ins[1][1]!="B" and ins[1][1]!="(B)" and ins[1][1]!="(A)":
            if "(" in ins[1][1]:
                ins[1][1],check=par_removal(ins[1][1])
                ins[1][1] = hex_to_dec(ins[1][1])
                if ins[1][1] > 255:
                    return f"Direccion fuera de rango permitido,{ins[1][1]}",-1
                if check:
                    ins[1][1]=par_adder(ins[1][1])
                string+="(Dir)"
            else:
                ins[1][1] = hex_to_dec(ins[1][1])
                if int(ins[1][1])>255:
                    return f"Literal fuera de rango permitido,{ins[1][1]}",-1
                string+="Lit"
        else:
            string +=ins[1][1]

    else:
        if "J" in ins[0]:
            if ins[1]!="A" and ins[1]!="B" and ins[1]!="(B)" and ins[1]!="(A)":
                if "(" not in ins[1]:
                    ins[1] = hex_to_dec(ins[1])
                    if ins[1]>largo-1:
                        return "Salto fuera de rango",-1 #Futuro labels
                    string+="Dir"
            else:
                string+=ins[1]

        else:
            if ins[1]!="A" and ins[1]!="B" and ins[1]!="(B)" and ins[1]!="(A)":
                if "(" in ins[1]:
                    ins[1],check=par_removal(ins[1])
                    ins[1] = hex_to_dec(ins[1])
                    if ins[1] > 255:
                        return f"Direccion fuera de rango permitido,{ins[1]}",-1
                    if check:
                        ins[1]=par_adder(ins[1])
                    string+="(Dir)"

                else:
                    ins[1] = hex_to_dec(ins[1])
                    if int(ins[1])>255:
                        return f"Literal fuera de rango permitido,{ins[1]}",-1
                    string+="Lit"
            else:
                string+=ins[1]

    if string in dic.keys():
        return True,string
    else:
        return f"Instruccion no existe, {string}",-1

def leer_archivo(nombre):
    file = open(nombre)
    inst = []
    for linea in file:
        linea = linea.split()
        if "," in linea[1]:
            linea[1] = linea[1].split(",")

        inst.append(linea)
    return inst

def revisor(archivo,dic):
    opc=[]
    instrucciones = leer_archivo(archivo)
    cont = 1
    verificador = True
    for ins in instrucciones:
        tmp,string = revisar_instruccion(ins,dic,len(instrucciones))
        if tmp != True:
            print(f"Error en la linea {cont} {tmp}")
            verificador = False
        else:
            opc.append(string)
        cont += 1
    if verificador:
        print (f"Lineas de codigo del archivo original: {cont-1}")

    return instrucciones,verificador,opc


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
                return aux
        else:
            if "(" in str(ins):
                aux,ver = par_removal(ins)
                aux = int(aux)
                return aux
            else:
                aux = int(ins)
                return aux
    return 0


# Main

string = "ej_max_distancia_errores.ass"
dic = opcodes(operaciones)
instrucciones,verificador,opc= revisor(string,dic)

if verificador:
    out = open(f"{string}.out","w")


    for ins in range(len(instrucciones)):
        if type(instrucciones[ins][1])==list:
            num = num_or_dir(instrucciones[ins][1][0],False)
            if num==0:
                num = num_or_dir(instrucciones[ins][1][0],False)
            num = num_or_dir(instrucciones[ins][1][1],False)
            if num==0:
                num = num_or_dir(instrucciones[ins][1][1],False)
            pass
        else:
            if "J" in instrucciones[ins][0]:
                num = num_or_dir(instrucciones[ins][1],True)
            else:
                num = num_or_dir(instrucciones[ins][1],False)

        out.write(dic[opc[ins]]+format(num,"08b")+"\n")



    out.close()
