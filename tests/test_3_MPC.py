"""
Pruebas del protocolo MPC básico (Punto 3)
=============================================

Cómo ejecutar:
    Desde la raíz del repositorio:
        python -m tests.test_3_MPC
    o bien, si se tiene pytest instalado:
        pytest tests/test_3_MPC.py -v

Como el reparto de notas usa números aleatorios (random.randint), las
pruebas no comparan las partes individuales contra un valor fijo, sino
que verifican las propiedades matemáticas que el protocolo debe cumplir
sin importar qué números aleatorios salgan: la suma reconstruida debe
coincidir con la suma real, y ninguna parte por sí sola debe revelar la
nota original.
"""

import sys
import os

RUTA_MODULO = os.path.join(
    os.path.dirname(__file__), "..", "src", "Criptografia"
)
sys.path.insert(0, os.path.abspath(RUTA_MODULO))

from punto3_MPC import (
    dividir_nota,
    repartir_notas,
    suma_servidor,
    reconstruir_suma_y_promedio,
)

M = 1000003


# ---------------------------------------------------------------------------
# Caso 1: ejemplo mínimo del enunciado del taller
# ---------------------------------------------------------------------------
def test_ejemplo_taller():
    # Entrada: notas=[40, 35, 50, 25]
    # Salida esperada: suma=150, promedio=37.5
    notas = [40, 35, 50, 25]
    s1, s2, s3 = repartir_notas(notas, M)
    S1, S2, S3 = suma_servidor(s1, M), suma_servidor(s2, M), suma_servidor(s3, M)
    suma_total, promedio = reconstruir_suma_y_promedio(S1, S2, S3, M, len(notas))

    assert suma_total == 150
    assert promedio == 37.5
    print("OK  test_ejemplo_taller")


# ---------------------------------------------------------------------------
# Caso 2: una sola nota se reconstruye exactamente
# ---------------------------------------------------------------------------
def test_una_sola_nota():
    x = 42
    s1, s2, s3 = dividir_nota(x, M)
    reconstruida = (s1 + s2 + s3) % M
    assert reconstruida == x
    print("OK  test_una_sola_nota")


# ---------------------------------------------------------------------------
# Caso 3: la suma reconstruida coincide con la suma real, repitiendo
# el experimento varias veces (para no depender de una sola tirada aleatoria)
# ---------------------------------------------------------------------------
def test_suma_reconstruida_coincide_con_suma_real():
    notas = [10, 20, 30, 40, 50]
    esperado = sum(notas)

    for _ in range(20):  # repetir por la aleatoriedad del reparto
        s1, s2, s3 = repartir_notas(notas, M)
        S1, S2, S3 = suma_servidor(s1, M), suma_servidor(s2, M), suma_servidor(s3, M)
        suma_total, _ = reconstruir_suma_y_promedio(S1, S2, S3, M, len(notas))
        assert suma_total == esperado
    print("OK  test_suma_reconstruida_coincide_con_suma_real")


# ---------------------------------------------------------------------------
# Caso 4: el promedio es correcto incluso cuando no es un número entero
# ---------------------------------------------------------------------------
def test_promedio_no_entero():
    notas = [10, 15]  # suma=25, promedio=12.5 (no debe redondearse a 12)
    s1, s2, s3 = repartir_notas(notas, M)
    S1, S2, S3 = suma_servidor(s1, M), suma_servidor(s2, M), suma_servidor(s3, M)
    suma_total, promedio = reconstruir_suma_y_promedio(S1, S2, S3, M, len(notas))

    assert suma_total == 25
    assert promedio == 12.5
    print("OK  test_promedio_no_entero")


# ---------------------------------------------------------------------------
# Caso 5: ninguna parte individual revela la nota original
# ---------------------------------------------------------------------------
def test_ninguna_parte_revela_la_nota():
    x = 37
    # Se repite varias veces porque el reparto es aleatorio; en ningún caso
    # una parte aislada debería coincidir con la nota original (la
    # probabilidad de que ocurra por azar es ínfima con M=1000003).
    for _ in range(20):
        s1, s2, s3 = dividir_nota(x, M)
        assert s1 != x
        assert s2 != x
        assert s3 != x
    print("OK  test_ninguna_parte_revela_la_nota")


# ---------------------------------------------------------------------------
# Caso 6: funciona con una lista de notas de cualquier tamaño (incluida 1)
# ---------------------------------------------------------------------------
def test_funciona_con_distintos_tamanos_de_lista():
    for notas in ([25], [10, 20, 30], [0, 50, 50, 0, 25]):
        s1, s2, s3 = repartir_notas(notas, M)
        S1, S2, S3 = suma_servidor(s1, M), suma_servidor(s2, M), suma_servidor(s3, M)
        suma_total, promedio = reconstruir_suma_y_promedio(S1, S2, S3, M, len(notas))
        assert suma_total == sum(notas)
        assert promedio == sum(notas) / len(notas)
    print("OK  test_funciona_con_distintos_tamanos_de_lista")


# ---------------------------------------------------------------------------
# Ejecutor simple (sin depender de pytest)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_ejemplo_taller()
    test_una_sola_nota()
    test_suma_reconstruida_coincide_con_suma_real()
    test_promedio_no_entero()
    test_ninguna_parte_revela_la_nota()
    test_funciona_con_distintos_tamanos_de_lista()
    print("\nTodas las pruebas pasaron correctamente.")