def calcular_probabilidad(letras,texto):
    longitud = len(texto) #Calculamos el total de los caracteres del texto
    probabilidad = {} #Creamos un diccionario vacio para almacenar la probabilidad de cada letra 
    for letra, numero_veces_aparece in letras.items(): #Como llamamos "letras.items()" nos devuelve la clave y el numero de veces que aparece, por lo cual para el for, necesitamos contener ambos valores
        probabilidad[letra] = numero_veces_aparece / longitud #Dividimos el numero de veces que aparece la letra por la longitud del texto, asi obteniendo la probabilidad, y procedemos a actualizar el diccionario con la letra y su probabilidad
    return probabilidad