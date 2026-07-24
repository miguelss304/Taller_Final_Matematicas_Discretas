import math
def calcular_entropia(probabilidades):
    entropia = 0 #Empezamos con un valor de 0
 
    for probabilidad in probabilidades.values(): #Recorremos el diccionario de probabilidades, y nos quedamos con los valores, que son las probabilidades de cada letra
        if probabilidad > 0: #Verificamos que la probabilidad sea mayor a 0, ya que si es 0, no podemos calcular el logaritmo
            entropia = entropia + probabilidad * math.log2(probabilidad) #Calculamos la entropia usando la formula de Shannon

    entropia = -entropia #La volvemos negativa, ya que la entropia es un valor positivo
    return entropia