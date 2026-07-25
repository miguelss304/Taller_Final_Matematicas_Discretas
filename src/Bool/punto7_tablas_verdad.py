"""
Tablas de verdad y circuitos lógicos
=======================================

Las tablas de verdad permiten revisar todas las posibilidades de una
expresión lógica: para cada combinación posible de valores de sus
variables (Verdadero/Falso), se calcula el resultado final. En
electrónica digital, cada una de estas expresiones se puede interpretar
directamente como un circuito hecho de compuertas AND, OR, NOT y XOR.

Expresiones incluidas (mínimo 3, como pide el enunciado):
    1. (A ∧ B) ∨ (¬C)
    2. (A ⊕ B) ∧ C
    3. (A ∨ B) ∧ (¬A ∨ C)

Estructura del archivo:
    1. Evaluación de cada expresión para valores concretos de A, B, C.
    2. Generación de la tabla de verdad completa (las 8 combinaciones).
    3. Evaluación de una entrada concreta pedida por el usuario.
    4. Programa principal.
"""

from itertools import product


# ---------------------------------------------------------------------------
# 1. Evaluación de cada expresión para valores concretos de A, B, C
# ---------------------------------------------------------------------------
def evaluar_expresion_1(a, b, c):
    """(A ∧ B) ∨ (¬C)"""
    return (a and b) or (not c)


def evaluar_expresion_2(a, b, c):
    """(A ⊕ B) ∧ C"""
    xor_ab = (a and not b) or (not a and b)  # A ⊕ B
    return xor_ab and c


def evaluar_expresion_3(a, b, c):
    """
    (A ∨ B) ∧ (¬A ∨ C)

    Nota: en la versión original de este código había un error aquí.
    El segundo término se calculaba como (A ∨ B) ∨ C en vez de
    (¬A ∨ C), porque se reutilizaba por error la variable del primer
    término. Se corrigió usando explícitamente "not a" en el segundo
    término, tal como pide la expresión.
    """
    termino1 = a or b            # (A ∨ B)
    termino2 = (not a) or c      # (¬A ∨ C)
    return termino1 and termino2


# Lista de expresiones a mostrar: (nombre, función, texto legible)
EXPRESIONES = [
    ("Expresión 1", evaluar_expresion_1, "(A ∧ B) ∨ (¬C)"),
    ("Expresión 2", evaluar_expresion_2, "(A ⊕ B) ∧ C"),
    ("Expresión 3", evaluar_expresion_3, "(A ∨ B) ∧ (¬A ∨ C)"),
]


# ---------------------------------------------------------------------------
# 2. Generación de la tabla de verdad completa (8 combinaciones para 3 variables)
# ---------------------------------------------------------------------------
def generar_tabla_verdad(funcion):
    """
    Genera todas las combinaciones posibles de A, B, C (2^3 = 8 filas) y
    calcula el resultado de `funcion` para cada una.

    Devuelve una lista de tuplas (a, b, c, resultado).
    """
    tabla = []
    for a, b, c in product([False, True], repeat=3):
        resultado = funcion(a, b, c)
        tabla.append((a, b, c, resultado))
    return tabla


def imprimir_tabla_verdad(nombre, texto_expresion, tabla):
    """Imprime en consola una tabla de verdad ya calculada, con formato de columnas."""
    print(f"\n{nombre}: {texto_expresion}")
    print(f"{'A':<7}{'B':<7}{'C':<7}{'Resultado':<10}")
    print("-" * 31)
    for a, b, c, resultado in tabla:
        print(f"{str(a):<7}{str(b):<7}{str(c):<7}{str(resultado):<10}")


# ---------------------------------------------------------------------------
# 3. Evaluación de una entrada concreta pedida al usuario
# ---------------------------------------------------------------------------
def pedir_valor(nombre_variable):
    """Pide por consola el valor de una variable booleana (F o V)."""
    valores_validos = {"F": False, "V": True}
    while True:
        entrada = input(f"{nombre_variable} (F = false, V = true): ").strip().upper()
        if entrada in valores_validos:
            return valores_validos[entrada]
        print("Valor inválido. Use 'F' o 'V'.")


def evaluar_entrada_concreta():
    """Pide A, B, C al usuario y muestra el resultado de las 3 expresiones."""
    print("\nIngrese los valores de las variables:")
    a = pedir_valor("A")
    b = pedir_valor("B")
    c = pedir_valor("C")

    print(f"\nResultados para A={a}, B={b}, C={c}:")
    for nombre, funcion, texto in EXPRESIONES:
        resultado = funcion(a, b, c)
        print(f"  {nombre}: {texto} = {resultado}")


# ---------------------------------------------------------------------------
# 4. Programa principal
# ---------------------------------------------------------------------------
def main():
    print("=" * 50)
    print("TABLAS DE VERDAD - EXPRESIONES LÓGICAS")
    print("=" * 50)

    # Se imprime la tabla de verdad completa de cada expresión
    for nombre, funcion, texto in EXPRESIONES:
        tabla = generar_tabla_verdad(funcion)
        imprimir_tabla_verdad(nombre, texto, tabla)

    # Además, se permite evaluar una entrada concreta pedida al usuario
    evaluar_entrada_concreta()


if __name__ == "__main__":
    main()