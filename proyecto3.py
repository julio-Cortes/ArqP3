# Declaracion de variables
# En la linea 240 aproximadamente hay un "main" donde esta el archivo que leera el programa
import sys
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

def transform_label_var(string, label, var, salto, lit):
    label_key = label.keys()
    var_key = list(var.keys())
    if string in label_key and salto == 1:
        return label[string]
    elif string in var_key and salto == 0:
        if lit == 1:
            return var_key.index(string) #CUANDO HAY PARENTESIS
        else:
            return var[string]           #CUANDO NO HAY PARENTESIS
    dat = 0
    try:
        if type(int(string)) == int:
            dat = 1
    except:
        pass
    if type(string) == str and dat == 0:
        if salto == 1:
            return -1
        elif salto == 0:
            return -2
    return string

def hex_to_dec(string):
    if type(string) == str:
        if  "#" in string:
            string = string.replace("#", "")
            return int(string, 16)
        else:
            return int(string)
    return string

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
def revisar_instruccion(ins,dic,largo,var,labels):
    string  = ins[0]+" "
    if type(ins[1])==list:

        valor_in = ins[1][0]

        if ins[1][0]!="A" and ins[1][0]!="B" and ins[1][0]!="(B)" and ins[1][0]!="(A)":
            if "(" in ins[1][0]:
                ins[1][0],check = par_removal(ins[1][0])
                ins[1][0] = transform_label_var(ins[1][0],labels,var,0,1)
                if ins[1][0] == -1:
                    return f"Etiqueta no existente en la instruccion {string}{valor_in}",-1
                if ins[1][0] == -2:
                    return f"Variable no existente en la instruccion {string}{valor_in}",-1
                ins[1][0] = hex_to_dec(ins[1][0])
                if ins[1][0] > 255:
                    return f"Direccion fuera de rango permitido,{ins[1][0]}",-1
                if check:
                    ins[1][0]=par_adder(ins[1][0])
                string+="(Dir)"
            else:
                ins[1][0] = transform_label_var(ins[1][0],labels,var,0,0)
                if ins[1][0] == -1:
                    return f"Etiqueta no existente en la instruccion {string}{valor_in}",-1
                if ins[1][0] == -2:
                    return f"Variable no existente en la instruccion {string}{valor_in}",-1
                ins[1][0] = hex_to_dec(ins[1][0])
                if int(ins[1][0])>255:
                    return f"Literal fuera de rango permitido,{ins[1][0]}",-1
                string+="Lit"

        else:
            string +=ins[1][0]

        string+=","

        if ins[1][1]!="A" and ins[1][1]!="B" and ins[1][1]!="(B)" and ins[1][1]!="(A)":
            valor_in = ins[1][1]
            if "(" in ins[1][1]:
                ins[1][1],check=par_removal(ins[1][1])
                ins[1][1] = transform_label_var(ins[1][1],labels,var,0,1)
                if ins[1][1] == -1:
                    return f"Etiqueta no existente en la instruccion {string}{valor_in}",-1
                if ins[1][1] == -2:
                    return f"Variable no existente en la instruccion {string}{valor_in}",-1
                ins[1][1] = hex_to_dec(ins[1][1])
                if ins[1][1] > 255:
                    return f"Direccion fuera de rango permitido,{ins[1][1]}",-1
                if check:
                    ins[1][1]=par_adder(ins[1][1])
                string+="(Dir)"
            else:
                ins[1][1] = transform_label_var(ins[1][1],labels,var,0,0)
                if ins[1][1] == -1:
                    return f"Etiqueta no existente en la instruccion {string}{valor_in}",-1
                if ins[1][1] == -2:
                    return f"Variable no existente en la instruccion {string}{valor_in}",-1
                ins[1][1] = hex_to_dec(ins[1][1])
                if int(ins[1][1])>255:
                    return f"Literal fuera de rango permitido,{ins[1][1]}",-1
                string+="Lit"
        else:
            string +=ins[1][1]

    else:
        valor_in = ins[1]
        if "J" in ins[0]:
            if ins[1]!="A" and ins[1]!="B" and ins[1]!="(B)" and ins[1]!="(A)":
                if "(" not in ins[1]:
                    ins[1] = transform_label_var(ins[1],labels,var,1,0)
                    if ins[1] == -1:
                        return f"Etiqueta no existente en la instruccion {string}{valor_in}",-1
                    if ins[1] == -2:
                        return f"Variable no existente en la instruccion {string}{valor_in}",-1
                    ins[1] = hex_to_dec(ins[1])
                    if ins[1]>largo:
                        return "Salto fuera de rango",-1 #Futuro labels
                    string+="Dir"
            else:
                string+=ins[1]

        else:
            if ins[1]!="A" and ins[1]!="B" and ins[1]!="(B)" and ins[1]!="(A)":
                if "(" in ins[1]:
                    ins[1],check=par_removal(ins[1])
                    ins[1] = transform_label_var(ins[1],labels,var,0,1)
                    if ins[1] == -1:
                        return f"Etiqueta no existente en la instruccion {string}{valor_in}",-1
                    if ins[1] == -2:
                        return f"Variable no existente en la instruccion {string}{valor_in}",-1
                    ins[1] = hex_to_dec(ins[1])
                    if ins[1] > 255:
                        return f"Direccion fuera de rango permitido,{ins[1]}",-1
                    if check:
                        ins[1]=par_adder(ins[1])
                    string+="(Dir)"

                else:
                    ins[1] = transform_label_var(ins[1],labels,var,0,0)
                    if ins[1] == -1:
                        return f"Etiqueta no existente en la instruccion {string}{valor_in}",-1
                    if ins[1] == -2:
                        return f"Variable no existente en la instruccion {string}{valor_in}",-1
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
    var = {}
    labels = {}
    cont_linea = 0
    inst = []
    in_code = 0
    for linea in file:
        if linea == "DATA:\n":
            continue
        if linea == "CODE:\n":
            in_code = 1
            continue
        linea = linea.split()
        if in_code == 1:
            try:
                if len(linea) <= 2:
                    if "," in linea[1]:
                        linea[1] = linea[1].split(",")
                    inst.append(linea)
                else:
                    fix_linea = []
                    labels[linea[0].replace(":","")] = cont_linea
                    fix_linea.append(linea[1])
                    fix_linea.append(linea[2])
                    if "," in fix_linea[1]:
                        fix_linea[1] = fix_linea[1].split(",")
                    inst.append(fix_linea)
                cont_linea+=1
            except:
                labels[linea[0].replace(":","")] = cont_linea
        else:
            if len(linea) > 1:
                var[linea[0]] = linea[1]
            else:
                var[linea[0]] = 0
    return inst, var, labels

def revisor(archivo,dic):
    opc=[]
    instrucciones, var, labels = leer_archivo(archivo)
    cont = 1
    verificador = True
    for ins in instrucciones:
        tmp,string = revisar_instruccion(ins,dic,len(instrucciones),var,labels)
        if tmp != True:
            print(f"Error en la linea {cont} {tmp}")
            verificador = False
        else:
            opc.append(string)
        cont += 1
    if verificador:
        print (f"Lineas de codigo del archivo original: {cont-1}")

    return instrucciones,verificador,opc, var, labels


"""
OP CODES PROCESSING
"""
def opcodes(operaciones):
    dic_ins = {}
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
            dic_ins[stringaux]=linea
            stringaux=""
            cont = 0
    return dic_ins

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
    return -1


# Main
if len(sys.argv) > 0:
    string = sys.argv[1]
    dic = opcodes(operaciones)
    instrucciones, verificador, opc, var, labels = revisor(string, dic)
    string = string.replace(".ass", "")


    if verificador:
        out = open(f"{string}.out", "w")

        for ins in range(len(instrucciones)):
            if type(instrucciones[ins][1]) == list:
                num = num_or_dir(instrucciones[ins][1][0], False)
                if num == -1:
                    num = num_or_dir(instrucciones[ins][1][0], False)
                if num != -1:
                    out.write(dic[opc[ins]] + format(num, "08b") + "\n")
                    continue
                num = num_or_dir(instrucciones[ins][1][1], False)
                if num == -1:
                    num = num_or_dir(instrucciones[ins][1][1], False)
                if num != -1:
                    out.write(dic[opc[ins]] + format(num, "08b") + "\n")
                    continue

            else:
                if "J" in instrucciones[ins][0]:
                    num = num_or_dir(instrucciones[ins][1], True)
                else:
                    num = num_or_dir(instrucciones[ins][1], False)
            if num == -1:
                num = 0

            out.write(dic[opc[ins]] + format(num, "08b") + "\n")

        out.close()

        out_mem = open(f"{string}.mem", "w")

        var_keys = var.keys()
        for dat in var_keys:
            num = hex_to_dec(var[dat])
            out_mem.write(format(num, "08b") + "\n")

        out_mem.close()
else:
    print ("File name missing")



