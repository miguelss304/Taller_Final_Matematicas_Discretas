"""
Primer simulador cuántico: bits, qubits y mediciones
=======================================================

Un bit clásico vale 0 o 1. Un qubit, en cambio, se representa como una
combinación (superposición) de los dos estados base:

    |psi> = alpha |0> + beta |1>

donde alpha y beta son números complejos, y |alpha|^2, |beta|^2 son las
probabilidades de medir 0 o 1 respectivamente (deben sumar 1).

Este archivo NO usa un computador cuántico real: es una simulación
matemática pequeña, representando el estado como un vector de 2 entradas
y las compuertas como matrices 2x2 que se multiplican por ese vector.

Compuertas incluidas:
    X = [[0, 1],       Z = [[1,  0],      H = 1/sqrt(2) * [[1,  1],
         [1, 0]]            [0, -1]]                        [1, -1]]

Estructura del archivo:
    1. Definición del estado inicial y de las compuertas (matrices).
    2. Aplicación de una compuerta a un estado (multiplicación matriz-vector).
    3. Cálculo de probabilidades de medir 0 o 1.
    4. Simulación de mediciones repetidas (colapso probabilístico).
    5. Casos de prueba obligatorios y programa principal.
"""

import cmath
import random


# ---------------------------------------------------------------------------
# 1. Estado inicial y definición de las compuertas
# ---------------------------------------------------------------------------
# Estado |0> = [1, 0], estado |1> = [0, 1]
ESTADO_0 = [1 + 0j, 0 + 0j]
ESTADO_1 = [0 + 0j, 1 + 0j]

RAIZ_2 = 2 ** 0.5

# Cada compuerta es una matriz 2x2 representada como lista de 2 filas,
# cada fila con 2 números complejos.
COMPUERTA_X = [[0 + 0j, 1 + 0j],
               [1 + 0j, 0 + 0j]]

COMPUERTA_Z = [[1 + 0j, 0 + 0j],
               [0 + 0j, -1 + 0j]]

COMPUERTA_H = [[1 / RAIZ_2 + 0j, 1 / RAIZ_2 + 0j],
               [1 / RAIZ_2 + 0j, -1 / RAIZ_2 + 0j]]


# ---------------------------------------------------------------------------
# 2. Aplicación de una compuerta a un estado (multiplicación matriz-vector)
# ---------------------------------------------------------------------------
def aplicar_compuerta(matriz, estado):
    """
    Aplica una compuerta (matriz 2x2) a un estado (vector de 2 entradas).

    Matemáticamente: nuevo_estado = matriz @ estado
    Cada entrada del nuevo estado es la suma de la fila correspondiente
    de la matriz, multiplicada elemento a elemento por el vector estado.
    """
    nuevo_estado = []
    for fila in matriz:
        entrada = sum(fila[j] * estado[j] for j in range(len(estado)))
        nuevo_estado.append(entrada)
    return nuevo_estado


# ---------------------------------------------------------------------------
# 3. Cálculo de probabilidades de medir 0 o 1
# ---------------------------------------------------------------------------
def calcular_probabilidades(estado):
    """
    Calcula las probabilidades de medir 0 y 1 a partir de un estado
    [alpha, beta]: prob(0) = |alpha|^2, prob(1) = |beta|^2.

    Se usa abs(numero_complejo) para obtener el módulo, y se eleva al
    cuadrado para obtener la probabilidad.
    """
    prob_0 = abs(estado[0]) ** 2
    prob_1 = abs(estado[1]) ** 2
    return prob_0, prob_1


# ---------------------------------------------------------------------------
# 4. Simulación de mediciones repetidas
# ---------------------------------------------------------------------------
def medir_una_vez(estado):
    """
    Simula una sola medición del qubit: devuelve 0 o 1, escogido al azar
    según las probabilidades del estado (colapso probabilístico).
    """
    prob_0, _ = calcular_probabilidades(estado)
    return 0 if random.random() < prob_0 else 1


def simular_mediciones(estado, cantidad=1000):
    """
    Simula `cantidad` mediciones independientes del mismo estado, y
    devuelve cuántas veces salió 0 y cuántas veces salió 1.
    """
    conteo = {0: 0, 1: 0}
    for _ in range(cantidad):
        resultado = medir_una_vez(estado)
        conteo[resultado] += 1
    return conteo


# ---------------------------------------------------------------------------
# 5. Casos de prueba obligatorios y programa principal
# ---------------------------------------------------------------------------
def mostrar_estado(nombre, estado):
    """Imprime el estado y sus probabilidades asociadas."""
    prob_0, prob_1 = calcular_probabilidades(estado)
    print(f"{nombre}: {estado}")
    print(f"  P(0) = {prob_0:.3f}, P(1) = {prob_1:.3f}")


def main():
    print("=" * 55)
    print("SIMULADOR BÁSICO DE UN QUBIT")
    print("=" * 55)

    # --- Caso 1: X|0> = |1> ---
    print("\nCaso 1: X|0>")
    resultado = aplicar_compuerta(COMPUERTA_X, ESTADO_0)
    mostrar_estado("X|0>", resultado)
    print(f"  ¿Es igual a |1>? {resultado == ESTADO_1}")

    # --- Caso 2: H|0> produce ~50%/50% ---
    print("\nCaso 2: H|0>")
    estado_h = aplicar_compuerta(COMPUERTA_H, ESTADO_0)
    mostrar_estado("H|0>", estado_h)

    conteo = simular_mediciones(estado_h, cantidad=1000)
    print(f"  Mediciones simuladas (1000): 0 -> {conteo[0]} veces, "
          f"1 -> {conteo[1]} veces")

    # --- Caso 3: HH|0> = |0> ---
    print("\nCaso 3: H(H|0>)")
    estado_hh = aplicar_compuerta(COMPUERTA_H, estado_h)
    mostrar_estado("HH|0>", estado_hh)
    # Se compara con una tolerancia pequeña por errores numéricos de punto flotante
    coincide = all(cmath.isclose(estado_hh[i], ESTADO_0[i], abs_tol=1e-9)
                    for i in range(2))
    print(f"  ¿Es igual a |0>? {coincide}")


if __name__ == "__main__":
    main()