"""
Pruebas del RSA de juguete (Punto 2)
=======================================

Cómo ejecutar:
    Desde la raíz del repositorio:
        python -m tests.test_2_rsa
    o bien, si se tiene pytest instalado:
        pytest tests/test_2_rsa.py -v
"""

import sys
import os

RUTA_MODULO = os.path.join(
    os.path.dirname(__file__), "..", "src", "Criptografia"
)
sys.path.insert(0, os.path.abspath(RUTA_MODULO))

from punto2_RSA import euclides_extendido, inverso_modular, generar_llaves, cifrar, descifrar


# ---------------------------------------------------------------------------
# Caso 1: caso de prueba obligatorio del enunciado del taller
# ---------------------------------------------------------------------------
def test_caso_obligatorio_taller():
    # Entrada: p=61, q=53, e=17, M=65
    # Salida esperada: n=3233, phi(n)=3120, d=2753, C=2790, M recuperado=65
    p, q, e, M = 61, 53, 17, 65

    n, phi_n, d = generar_llaves(p, q, e)
    assert n == 3233
    assert phi_n == 3120
    assert d == 2753

    C = cifrar(M, e, n)
    assert C == 2790

    M_recuperado = descifrar(C, d, n)
    assert M_recuperado == 65
    print("OK  test_caso_obligatorio_taller")


# ---------------------------------------------------------------------------
# Caso 2: el algoritmo de Euclides extendido calcula el gcd correcto
# ---------------------------------------------------------------------------
def test_euclides_extendido_gcd():
    # Entrada: a=17, b=3120 (coprimos, gcd debe ser 1)
    gcd, x, y = euclides_extendido(17, 3120)
    assert gcd == 1
    # La identidad de Bézout debe cumplirse: a*x + b*y = gcd
    assert 17 * x + 3120 * y == 1
    print("OK  test_euclides_extendido_gcd")


# ---------------------------------------------------------------------------
# Caso 3: el inverso modular calculado realmente invierte a e
# ---------------------------------------------------------------------------
def test_inverso_modular_correcto():
    e, phi = 17, 3120
    d = inverso_modular(e, phi)
    assert (e * d) % phi == 1
    print("OK  test_inverso_modular_correcto")


# ---------------------------------------------------------------------------
# Caso 4: e inválido (gcd(e, phi) != 1) debe lanzar ValueError
# ---------------------------------------------------------------------------
def test_e_invalido_lanza_error():
    # phi(n) para p=61, q=53 es 3120 (múltiplo de 2), así que e=2 no es
    # válido porque gcd(2, 3120) = 2 != 1.
    try:
        generar_llaves(61, 53, 2)
        assert False, "Se esperaba un ValueError"
    except ValueError:
        print("OK  test_e_invalido_lanza_error")


# ---------------------------------------------------------------------------
# Caso 5: cifrar y luego descifrar recupera el mensaje original,
# probado con otro conjunto de primos y otro mensaje
# ---------------------------------------------------------------------------
def test_cifrar_y_descifrar_es_identidad():
    p, q, e, M = 7, 11, 7, 5  # n=77, phi=60, gcd(7,60)=1
    n, phi_n, d = generar_llaves(p, q, e)

    C = cifrar(M, e, n)
    M_recuperado = descifrar(C, d, n)

    assert M_recuperado == M
    print("OK  test_cifrar_y_descifrar_es_identidad")


# ---------------------------------------------------------------------------
# Caso 6: n y phi(n) se calculan correctamente para otro par de primos
# ---------------------------------------------------------------------------
def test_n_y_phi_correctos():
    p, q = 7, 11
    n, phi_n, _ = generar_llaves(p, q, e=7)
    assert n == 77           # n = p*q = 7*11
    assert phi_n == 60        # phi(n) = (p-1)(q-1) = 6*10
    print("OK  test_n_y_phi_correctos")


# ---------------------------------------------------------------------------
# Ejecutor simple (sin depender de pytest)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_caso_obligatorio_taller()
    test_euclides_extendido_gcd()
    test_inverso_modular_correcto()
    test_e_invalido_lanza_error()
    test_cifrar_y_descifrar_es_identidad()
    test_n_y_phi_correctos()
    print("\nTodas las pruebas pasaron correctamente.")