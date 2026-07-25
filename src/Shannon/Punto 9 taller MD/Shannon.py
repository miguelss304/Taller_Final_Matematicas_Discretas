from Contar import contar_letras
from Probabilidad import calcular_probabilidad
from Entropia import calcular_entropia 
from Comparar import comparar_textos

textos = [] #Procedemos a crear una lista vacia para los textos

cantidad = int(input("Ingrese la cantidad de textos que desea comparar ")) #Se le pide al usuario que ingrese la cantidad de los textos

for i in range(cantidad): 
    texto = input(f"Ingrese el texto {i+1}: ") #Pedimos al usuario que ingrese el texto, y le mostramos en cual de los textos va
    textos.append(texto) #Agregamos el texto a la lista de textos


comparar_textos(textos) #Llamamos a la funcion comparar_textos, y le pasamos la lista de textos que el usuario ingreso