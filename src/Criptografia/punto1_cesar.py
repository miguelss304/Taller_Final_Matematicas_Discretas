"""
Cifrado César
=============

El cifrado César desplaza cada letra del alfabeto una cantidad fija de
posiciones (k). Para cifrar se desplaza hacia adelante, para descifrar se
desplaza la misma cantidad pero hacia atrás (el desplazamiento inverso).

Estructura del archivo:
    1. Alfabeto base (constante).
    2. Función auxiliar para construir la tabla de sustitución (cifrado
       o descifrado, según el signo del desplazamiento).
    3. Función para aplicar esa tabla a un texto.
    4. Funciones de cifrar/descifrar que piden los datos al usuario.
    5. Menú principal.
"""

# ---------------------------------------------------------------------------
# 1. Alfabeto base
# ---------------------------------------------------------------------------
LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ---------------------------------------------------------------------------
# 2. Construcción de la tabla de sustitución
# ---------------------------------------------------------------------------
def construir_tabla(k, direccion):
    """
    Construye un diccionario {letra_original: letra_sustituta} desplazando
    el alfabeto k posiciones.

    direccion=1  -> cifrar (desplaza hacia adelante:  A -> letra en pos A+k)
    direccion=-1 -> descifrar (desplaza hacia atrás:  A -> letra en pos A-k)

    Se usa aritmética modular (% 26) para que el desplazamiento "dé la
    vuelta" al llegar a la Z (o antes de la A al descifrar).
    """
    tabla = {}
    for posicion, letra in enumerate(LETRAS):
        nueva_posicion = (posicion + direccion * k) % 26
        tabla[letra] = LETRAS[nueva_posicion]
    return tabla


# ---------------------------------------------------------------------------
# 3. Aplicar la tabla de sustitución a un texto completo
# ---------------------------------------------------------------------------
def aplicar_tabla(texto, tabla):
    """
    Recorre el texto letra por letra y la reemplaza según la tabla.
    Los caracteres que no están en la tabla (espacios, signos de
    puntuación, números) se dejan tal cual, sin modificarlos.
    """
    resultado = []
    for letra in texto:
        resultado.append(tabla.get(letra, letra))
    return "".join(resultado)


# ---------------------------------------------------------------------------
# 4. Funciones puras de cifrado/descifrado (fáciles de probar con tests)
# ---------------------------------------------------------------------------
def cifrar_texto(texto, k):
    """Cifra un texto (ya en mayúsculas) con desplazamiento k. Función pura."""
    tabla = construir_tabla(k, direccion=1)
    return aplicar_tabla(texto, tabla)


def descifrar_texto(texto, k):
    """Descifra un texto (ya en mayúsculas) con desplazamiento k. Función pura."""
    tabla = construir_tabla(k, direccion=-1)
    return aplicar_tabla(texto, tabla)


# ---------------------------------------------------------------------------
# 5. Cifrado y descifrado interactivos (piden datos al usuario por consola)
# ---------------------------------------------------------------------------
def cifrar_mensaje():
    """Pide un mensaje y un desplazamiento k, y muestra el texto cifrado."""
    texto = input("Ingrese el mensaje a cifrar: ").upper()
    k = int(input("Ingrese el valor de k: "))
    print("Mensaje cifrado:", cifrar_texto(texto, k))


def descifrar_mensaje():
    """Pide un mensaje cifrado y un desplazamiento k, y muestra el original."""
    texto = input("Ingrese el mensaje a descifrar: ").upper()
    k = int(input("Ingrese el valor de k: "))
    print("Mensaje descifrado:", descifrar_texto(texto, k))


def fuerza_bruta(texto):
    """
    Prueba los 26 desplazamientos posibles y muestra cada resultado.
    Útil cuando no se conoce k: el usuario revisa cuál de las 26 líneas
    tiene sentido en español.
    """
    texto = texto.upper()
    for k in range(26):
        print(f"k={k:2d}: {descifrar_texto(texto, k)}")


# ---------------------------------------------------------------------------
# 6. Menú principal
# ---------------------------------------------------------------------------
def main():
    opcion = int(input(
        "Ingrese si desea cifrar o descifrar el mensaje:\n"
        " 1. Cifrar\n"
        " 2. Descifrar\n"
        " 3. Probar todos los desplazamientos (fuerza bruta)\n"
    ))

    if opcion == 1:
        cifrar_mensaje()
    elif opcion == 2:
        descifrar_mensaje()
    elif opcion == 3:
        texto = input("Ingrese el mensaje cifrado: ")
        fuerza_bruta(texto)
    else:
        print("Opción no válida.")


if __name__ == "__main__":
    main()