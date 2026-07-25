"""
Shannon: medir información en un mensaje
===========================================

Claude Shannon propuso una forma de medir cuánta información (o
incertidumbre) contiene una fuente de datos. Un mensaje muy repetitivo
tiene menor entropía que uno donde los símbolos están más distribuidos,
porque hay menos "sorpresa" al leer cada nuevo carácter.

Fórmula de la entropía de Shannon:
    H = - sum( p_i * log2(p_i) )   para cada símbolo i

Estructura del archivo:
    1. Conteo de apariciones de cada carácter en un texto.
    2. Cálculo de la probabilidad de cada carácter.
    3. Cálculo de la entropía a partir de esas probabilidades.
    4. Comparación de varios textos, mostrando cuál tiene mayor entropía.
    5. Entrada de datos por consola.
"""

import math


# ---------------------------------------------------------------------------
# 1. Conteo de apariciones de cada carácter
# ---------------------------------------------------------------------------
def contar_letras(texto):
    """
    Cuenta cuántas veces aparece cada carácter en el texto.
    Devuelve un diccionario {caracter: numero_de_apariciones}.
    """
    letras = {}
    for caracter in texto:
        if caracter in letras:
            letras[caracter] += 1
        else:
            letras[caracter] = 1
    return letras


# ---------------------------------------------------------------------------
# 2. Cálculo de la probabilidad de cada carácter
# ---------------------------------------------------------------------------
def calcular_probabilidad(conteo_letras, texto):
    """
    Calcula la probabilidad de cada carácter como:
        probabilidad = numero_de_apariciones / longitud_total_del_texto

    Devuelve un diccionario {caracter: probabilidad}.
    """
    longitud = len(texto)
    probabilidad = {}
    for letra, numero_veces_aparece in conteo_letras.items():
        probabilidad[letra] = numero_veces_aparece / longitud
    return probabilidad


# ---------------------------------------------------------------------------
# 3. Cálculo de la entropía de Shannon
# ---------------------------------------------------------------------------
def calcular_entropia(probabilidades):
    """
    Calcula la entropía de Shannon: H = -sum(p_i * log2(p_i)).

    Se omiten las probabilidades iguales a 0 porque log2(0) no está
    definido (en la práctica esto no ocurre, ya que solo se incluyen
    en el diccionario los símbolos que sí aparecieron en el texto).
    """
    entropia = 0
    for probabilidad in probabilidades.values():
        if probabilidad > 0:
            entropia += probabilidad * math.log2(probabilidad)
    return -entropia  # la entropía se expresa como un valor positivo


# ---------------------------------------------------------------------------
# 4. Comparación de varios textos
# ---------------------------------------------------------------------------
def analizar_texto(texto):
    """
    Calcula, para un solo texto, el conteo de letras, sus probabilidades
    y su entropía. Devuelve los tres resultados juntos.
    """
    cantidad_letras = contar_letras(texto)
    probabilidad_letras = calcular_probabilidad(cantidad_letras, texto)
    entropia = calcular_entropia(probabilidad_letras)
    return cantidad_letras, probabilidad_letras, entropia


def mostrar_analisis(texto, cantidad_letras, probabilidad_letras, entropia):
    """Imprime en consola el detalle del análisis de un texto."""
    print(f"Texto: {texto}")

    print("Cantidad de letras:")
    for clave, valor in cantidad_letras.items():
        print(f" '{clave}': {valor}")

    print("Probabilidades:")
    for clave, valor in probabilidad_letras.items():
        print(f" '{clave}': {valor:.3f}")

    print(f"Entropía: {entropia:.3f}")


def comparar_textos(textos):
    """
    Recorre una lista de textos, calcula la entropía de cada uno y
    reporta cuál tiene la mayor entropía (el más "impredecible").
    """
    mejor_texto = ""
    mejor_entropia = -1  # cualquier entropía real (>= 0) será mayor que esto

    for texto in textos:
        cantidad_letras, probabilidad_letras, entropia = analizar_texto(texto)
        mostrar_analisis(texto, cantidad_letras, probabilidad_letras, entropia)

        if entropia > mejor_entropia:
            mejor_entropia = entropia
            mejor_texto = texto

        print()  # línea en blanco entre textos, para mayor claridad

    print(f"El texto con mayor entropía es: '{mejor_texto}' "
          f"con una entropía de {mejor_entropia:.3f}")


# ---------------------------------------------------------------------------
# 5. Entrada de datos por consola
# ---------------------------------------------------------------------------
def main():
    cantidad = int(input("Ingrese la cantidad de textos que desea comparar: "))

    textos = []
    for i in range(cantidad):
        texto = input(f"Ingrese el texto {i + 1}: ")
        textos.append(texto)

    comparar_textos(textos)


if __name__ == "__main__":
    main()