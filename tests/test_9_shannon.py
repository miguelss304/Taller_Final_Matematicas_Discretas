"""
Pruebas de entropía de Shannon (Punto 9)
===========================================

Cómo ejecutar:
    Desde la raíz del repositorio:
        python -m tests.test_9_shannon
    o bien, si se tiene pytest instalado:
        pytest tests/test_9_shannon.py -v
"""

import math
import sys
import os

RUTA_MODULO = os.path.join(
    os.path.dirname(__file__), "..", "src", "Cuantica"
)
sys.path.insert(0, os.path.abspath(RUTA_MODULO))

from punto9_shannon import (
    contar_letras,
    calcular_probabilidad,
    calcular_entropia,
    analizar_texto,
)


# ---------------------------------------------------------------------------
# Caso 1: conteo de letras básico
# ---------------------------------------------------------------------------
def test_contar_letras():
    # Entrada: "AAB"
    # Salida esperada: {'A': 2, 'B': 1}
    resultado = contar_letras("AAB")
    assert resultado == {"A": 2, "B": 1}
    print("OK  test_contar_letras")


# ---------------------------------------------------------------------------
# Caso 2: probabilidad calculada correctamente a partir del conteo
# ---------------------------------------------------------------------------
def test_calcular_probabilidad():
    conteo = {"A": 2, "B": 2}
    probabilidad = calcular_probabilidad(conteo, "AABB")
    assert probabilidad == {"A": 0.5, "B": 0.5}
    print("OK  test_calcular_probabilidad")


# ---------------------------------------------------------------------------
# Caso 3: texto totalmente repetitivo -> entropía debe ser 0
# ---------------------------------------------------------------------------
def test_entropia_texto_repetitivo():
    # Un solo símbolo con probabilidad 1 aporta -1*log2(1) = 0
    _, _, entropia = analizar_texto("AAAAA")
    assert math.isclose(entropia, 0.0, abs_tol=1e-9)
    print("OK  test_entropia_texto_repetitivo")


# ---------------------------------------------------------------------------
# Caso 4: dos símbolos equiprobables -> entropía debe ser exactamente 1 bit
# ---------------------------------------------------------------------------
def test_entropia_dos_simbolos_equiprobables():
    # "ABAB" tiene A y B con probabilidad 0.5 cada uno
    # H = -(0.5*log2(0.5) + 0.5*log2(0.5)) = 1.0
    _, _, entropia = analizar_texto("ABAB")
    assert math.isclose(entropia, 1.0, abs_tol=1e-9)
    print("OK  test_entropia_dos_simbolos_equiprobables")


# ---------------------------------------------------------------------------
# Caso 5: un texto más variado debe tener mayor entropía que uno repetitivo
# ---------------------------------------------------------------------------
def test_texto_variado_mayor_entropia_que_repetitivo():
    _, _, entropia_repetitivo = analizar_texto("AAAAAAAAAA")
    _, _, entropia_variado = analizar_texto("HOLA MUNDO")
    assert entropia_variado > entropia_repetitivo
    print("OK  test_texto_variado_mayor_entropia_que_repetitivo")


# ---------------------------------------------------------------------------
# Caso 6: calcular_entropia funciona directamente con un diccionario
# de probabilidades (sin pasar por contar_letras / calcular_probabilidad)
# ---------------------------------------------------------------------------
def test_calcular_entropia_directo():
    # Cuatro símbolos equiprobables -> H = log2(4) = 2.0
    probabilidades = {"A": 0.25, "B": 0.25, "C": 0.25, "D": 0.25}
    entropia = calcular_entropia(probabilidades)
    assert math.isclose(entropia, 2.0, abs_tol=1e-9)
    print("OK  test_calcular_entropia_directo")


# ---------------------------------------------------------------------------
# Ejecutor simple (sin depender de pytest)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_contar_letras()
    test_calcular_probabilidad()
    test_entropia_texto_repetitivo()
    test_entropia_dos_simbolos_equiprobables()
    test_texto_variado_mayor_entropia_que_repetitivo()
    test_calcular_entropia_directo()
    print("\nTodas las pruebas pasaron correctamente.")