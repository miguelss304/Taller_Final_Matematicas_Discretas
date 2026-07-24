from Contar import contar_letras
from Probabilidad import calcular_probabilidad
from Entropia import calcular_entropia 

def comparar_textos(textos):
    mejor_texto = ""
    mejor_entropia = -1 #Se inicia con -1 para que cualquier entropia calculada sea mayor a este numero

    for texto in textos: #El for recorre la lista de textos y calcula la cantidad de letras, la probabilidad y la entropia
        cantidad_letras = contar_letras(texto)
        probabilidad_letras = calcular_probabilidad(cantidad_letras, texto)
        entropia = calcular_entropia(probabilidad_letras)

        print(f"Texto: {texto}") #Imprime cual texto es

        print("Cantidad de letras:")
        for clave, valor in cantidad_letras.items():
            print(f" '{clave}': {valor}") #Imprime la cantidad de letras de cada texto

        print("Probabilidades:")
        for clave, valor in probabilidad_letras.items():
            print(f" '{clave}': {valor:.3f}") #Imprime la probabilidad de cada letra de cada texto, usando solo 3 decimales

        print(f"Entropía: {entropia:.3f}")

        if entropia > mejor_entropia:
            mejor_entropia = entropia #Se compara los textos por mejor entropia y actualiza las variables
            mejor_texto = texto

    print(f"El texto con mayor entropía es: '{mejor_texto}' con una entropía de {mejor_entropia:.3f}")
