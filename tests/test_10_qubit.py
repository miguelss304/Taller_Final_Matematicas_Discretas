"""
Pruebas del simulador básico de un qubit (Punto 10)
=======================================================

Cómo ejecutar:
    Desde la raíz del repositorio:
        python -m tests.test_10_qubit
    o bien, si se tiene pytest instalado:
        pytest tests/test_10_qubit.py -v
"""

import cmath
import sys
import os

RUTA_MODULO = os.path.join(os.path.dirname(__file__), "..", "src", "Cuantica")
sys.path.insert(0, os.path.abspath(RUTA_MODULO))

from punto10_qubit import (
    ESTADO_0,
    ESTADO_1,
    COMPUERTA_X,
    COMPUERTA_Z,
    COMPUERTA_H,
    aplicar_compuerta,
    calcular_probabilidades,
    simular_mediciones,
)


def estados_son_iguales(estado_a, estado_b, tolerancia=1e-9):
    """Compara dos estados componente a componente con tolerancia numérica."""
    return all(
        cmath.isclose(estado_a[i], estado_b[i], abs_tol=tolerancia)
        for i in range(len(estado_a))
    )


# ---------------------------------------------------------------------------
# Caso 1 (obligatorio): X|0> = |1>
# ---------------------------------------------------------------------------
def test_x_sobre_0_da_1():
    resultado = aplicar_compuerta(COMPUERTA_X, ESTADO_0)
    assert estados_son_iguales(resultado, ESTADO_1)
    print("OK  test_x_sobre_0_da_1")


# ---------------------------------------------------------------------------
# Caso 2 (obligatorio): H|0> produce probabilidades cercanas a 50%/50%
# ---------------------------------------------------------------------------
def test_h_sobre_0_da_probabilidades_50_50():
    estado_h = aplicar_compuerta(COMPUERTA_H, ESTADO_0)
    prob_0, prob_1 = calcular_probabilidades(estado_h)
    assert cmath.isclose(prob_0, 0.5, abs_tol=1e-9)
    assert cmath.isclose(prob_1, 0.5, abs_tol=1e-9)
    print("OK  test_h_sobre_0_da_probabilidades_50_50")


# ---------------------------------------------------------------------------
# Caso 3 (obligatorio): HH|0> = |0>, salvo errores numéricos pequeños
# ---------------------------------------------------------------------------
def test_hh_sobre_0_regresa_a_0():
    estado_h = aplicar_compuerta(COMPUERTA_H, ESTADO_0)
    estado_hh = aplicar_compuerta(COMPUERTA_H, estado_h)
    assert estados_son_iguales(estado_hh, ESTADO_0)
    print("OK  test_hh_sobre_0_regresa_a_0")


# ---------------------------------------------------------------------------
# Caso 4: X|1> = |0> (aplicar X dos veces regresa al estado original)
# ---------------------------------------------------------------------------
def test_x_es_su_propia_inversa():
    estado_x = aplicar_compuerta(COMPUERTA_X, ESTADO_0)
    estado_xx = aplicar_compuerta(COMPUERTA_X, estado_x)
    assert estados_son_iguales(estado_xx, ESTADO_0)
    print("OK  test_x_es_su_propia_inversa")


# ---------------------------------------------------------------------------
# Caso 5: Z|0> = |0> (Z no afecta al estado base |0>, solo cambia la fase de |1>)
# ---------------------------------------------------------------------------
def test_z_sobre_0_no_cambia_el_estado():
    resultado = aplicar_compuerta(COMPUERTA_Z, ESTADO_0)
    assert estados_son_iguales(resultado, ESTADO_0)
    print("OK  test_z_sobre_0_no_cambia_el_estado")


# ---------------------------------------------------------------------------
# Caso 6: las probabilidades de cualquier estado válido deben sumar 1
# ---------------------------------------------------------------------------
def test_probabilidades_suman_1():
    for estado in (ESTADO_0, ESTADO_1, aplicar_compuerta(COMPUERTA_H, ESTADO_0)):
        prob_0, prob_1 = calcular_probabilidades(estado)
        assert cmath.isclose(prob_0 + prob_1, 1.0, abs_tol=1e-9)
    print("OK  test_probabilidades_suman_1")


# ---------------------------------------------------------------------------
# Caso 7: simular 1000 mediciones de |0> siempre da 0 (estado sin superposición)
# ---------------------------------------------------------------------------
def test_mediciones_estado_0_siempre_da_0():
    conteo = simular_mediciones(ESTADO_0, cantidad=1000)
    assert conteo[0] == 1000
    assert conteo[1] == 0
    print("OK  test_mediciones_estado_0_siempre_da_0")


# ---------------------------------------------------------------------------
# Caso 8: simular 1000 mediciones de H|0> da una proporción cercana a 50/50
# (con margen amplio, ya que es un proceso aleatorio)
# ---------------------------------------------------------------------------
def test_mediciones_h_sobre_0_cercanas_a_mitad():
    estado_h = aplicar_compuerta(COMPUERTA_H, ESTADO_0)
    conteo = simular_mediciones(estado_h, cantidad=1000)
    # Con 1000 mediciones y probabilidad real 0.5, es extremadamente
    # improbable que el conteo de 0s esté fuera del rango [400, 600].
    assert 400 <= conteo[0] <= 600
    assert conteo[0] + conteo[1] == 1000
    print("OK  test_mediciones_h_sobre_0_cercanas_a_mitad")


# ---------------------------------------------------------------------------
# Ejecutor simple (sin depender de pytest)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_x_sobre_0_da_1()
    test_h_sobre_0_da_probabilidades_50_50()
    test_hh_sobre_0_regresa_a_0()
    test_x_es_su_propia_inversa()
    test_z_sobre_0_no_cambia_el_estado()
    test_probabilidades_suman_1()
    test_mediciones_estado_0_siempre_da_0()
    test_mediciones_h_sobre_0_cercanas_a_mitad()
    print("\nTodas las pruebas pasaron correctamente.")