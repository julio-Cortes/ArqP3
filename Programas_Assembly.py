# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 18:13:06 2020

@author: rafae
"""

#ASSEMBLYS

#Contar pares
inicio = 0 #DEFINICION DE VARIABLES
fin = 7  
pares = 0  #REGISTRO A
mem = [2,5,6,4,3,1,5,7,8,9,9] #MEMORIA

while inicio < fin:  #2
    mem[inicio] = mem[inicio] & 1 #1
    if mem[inicio] == 0: #2
        pares+= 1 #1
    inicio+=1 #1

print(pares)

"""
MOV INICIO,4
MOV FIN,8
AND (INICIO),1
CMP (INICIO),0
JNE 7
ADD A,1
ADD INICIO,1
CMP INICIO,FIN
JLE 1
"""