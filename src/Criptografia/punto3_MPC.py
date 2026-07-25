"""
MPC básico: calcular un promedio sin mostrar los datos
========================================================

Simula un protocolo de suma secreta con tres servidores, para ilustrar
la idea central de la Computación Multipartita Segura (MPC): varias
partes pueden calcular un resultado conjunto (aquí, una suma y un
promedio) sin que ninguna de ellas vea los datos individuales completos.

Idea matemática:
    Cada nota x se divide en tres partes aleatorias (s1, s2, s3) tales
    que:
                x ≡ s1 + s2 + s3  (mód M)

    Cada servidor recibe una sola parte de cada nota. Ninguna parte por
    sí sola revela nada sobre x (ver docs/ para el detalle). Solo cuando
    se suman las tres partes (mód M) se recupera la nota original.

Estructura del archivo:
    1. División de una nota en 3 partes secretas.
    2. Reparto de una lista de notas entre 3 "servidores".
    3. Suma que calcula cada servidor sobre sus propias partes.
    4. Reconstrucción de la suma total y el promedio.
    5. Entrada de datos por consola (validación incluida).
    6. Programa principal.
"""

import random


# ---------------------------------------------------------------------------
# 1. División de una nota en 3 partes secretas
# ---------------------------------------------------------------------------
def dividir_nota(x, M):
    """
    Divide una nota x en tres partes aleatorias (s1, s2, s3) tales que
    (s1 + s2 + s3) % M == x % M.

    s1 y s2 se generan al azar; s3 se calcula para que la suma cuadre.
    Ninguna de las tres partes por separado revela el valor de x.
    """
    s1 = random.randint(0, M - 1)
    s2 = random.randint(0, M - 1)
    s3 = (x - s1 - s2) % M
    return s1, s2, s3


# ---------------------------------------------------------------------------
# 2. Reparto de una lista completa de notas entre los 3 servidores
# ---------------------------------------------------------------------------
def repartir_notas(notas, M):
    """
    Reparte cada nota de la lista entre tres servidores.

    Devuelve tres listas (servidor1, servidor2, servidor3), donde
    servidorN[i] es la parte que le corresponde a ese servidor de la
    nota notas[i]. Cada servidor solo ve su propia lista de partes,
    nunca las notas originales.
    """
    servidor1, servidor2, servidor3 = [], [], []

    for nota in notas:
        s1, s2, s3 = dividir_nota(nota, M)
        servidor1.append(s1)
        servidor2.append(s2)
        servidor3.append(s3)

    return servidor1, servidor2, servidor3


# ---------------------------------------------------------------------------
# 3. Suma que calcula cada servidor sobre sus propias partes
# ---------------------------------------------------------------------------
def suma_servidor(partes_servidor, M):
    """Suma (mód M) todas las partes que tiene un servidor."""
    return sum(partes_servidor) % M


# ---------------------------------------------------------------------------
# 4. Reconstrucción de la suma total y el promedio
# ---------------------------------------------------------------------------
def reconstruir_suma_y_promedio(S1, S2, S3, M, cantidad_notas):
    """
    Combina las tres sumas parciales (una por servidor) para recuperar
    la suma total real de las notas, y calcula el promedio.

    Se usa división real (no entera) para que el promedio sea exacto,
    por ejemplo 150 / 4 = 37.5 y no 37.
    """
    suma_total = (S1 + S2 + S3) % M
    promedio = suma_total / cantidad_notas
    return suma_total, promedio


# ---------------------------------------------------------------------------
# 5. Entrada de datos por consola, con validación
# ---------------------------------------------------------------------------
def ingresar_notas(cantidad):
    """Pide por consola `cantidad` notas, validando que estén entre 0 y 50."""
    notas = []
    print("Ingrese las notas (de 0 a 50):")
    for i in range(cantidad):
        while True:
            nota = int(input(f"Nota {i + 1}: "))
            if 0 <= nota <= 50:
                notas.append(nota)
                break
            print("Nota inválida. Por favor, ingrese una nota del 0 al 50.")
    return notas


def pedir_cantidad_notas():
    """Pide por consola cuántas notas se van a ingresar (debe ser > 0)."""
    cantidad = int(input("Ingrese el total de notas a ingresar: "))
    while cantidad <= 0:
        print("El número de notas debe ser mayor que cero.")
        cantidad = int(input("Ingrese el total de notas a ingresar: "))
    return cantidad


# ---------------------------------------------------------------------------
# 6. Programa principal
# ---------------------------------------------------------------------------
def main():
    M = 1000003  # módulo, suficientemente grande frente a las notas (0-50)

    cantidad = pedir_cantidad_notas()
    notas = ingresar_notas(cantidad)

    # Cada nota se reparte en tres partes; cada servidor solo recibe su parte.
    servidor1, servidor2, servidor3 = repartir_notas(notas, M)

    # Cada servidor calcula la suma de sus propias partes, sin ver las notas.
    S1 = suma_servidor(servidor1, M)
    S2 = suma_servidor(servidor2, M)
    S3 = suma_servidor(servidor3, M)

    # Solo al combinar las tres sumas parciales se recupera el resultado real.
    suma_total, promedio = reconstruir_suma_y_promedio(S1, S2, S3, M, cantidad)

    print(f"Suma total de las notas: {suma_total}")
    print(f"Promedio de las notas: {promedio}")


if __name__ == "__main__":
    main()