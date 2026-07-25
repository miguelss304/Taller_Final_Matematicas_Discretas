"""
Pruebas de tablas de verdad y circuitos lógicos (Punto 7)
=============================================================

Cómo ejecutar:
    Desde la raíz del repositorio:
        python -m tests.test_7_tablas_verdad
    o bien, si se tiene pytest instalado:
        pytest tests/test_7_tablas_verdad.py -v
"""

import sys
import os

RUTA_MODULO = os.path.join(os.path.dirname(__file__), "..", "src", "Bool")
sys.path.insert(0, os.path.abspath(RUTA_MODULO))

from punto7_tablas_verdad import (
    evaluar_expresion_1,
    evaluar_expresion_2,
    evaluar_expresion_3,
    generar_tabla_verdad,
)


# ---------------------------------------------------------------------------
# Caso 1: expresión 1 -> (A ∧ B) ∨ (¬C), caso donde C=False domina (resultado True)
# ---------------------------------------------------------------------------
def test_expresion_1_c_falso_domina():
    # Entrada: A=False, B=False, C=False -> (F∧F)∨(¬F) = F∨V = True
    assert evaluar_expresion_1(False, False, False) is True
    print("OK  test_expresion_1_c_falso_domina")


# ---------------------------------------------------------------------------
# Caso 2: expresión 1 -> caso donde da False
# ---------------------------------------------------------------------------
def test_expresion_1_resultado_falso():
    # Entrada: A=False, B=False, C=True -> (F∧F)∨(¬V) = F∨F = False
    assert evaluar_expresion_1(False, False, True) is False
    print("OK  test_expresion_1_resultado_falso")


# ---------------------------------------------------------------------------
# Caso 3: expresión 2 -> (A ⊕ B) ∧ C, verificando el comportamiento del XOR
# ---------------------------------------------------------------------------
def test_expresion_2_xor_correcto():
    # A=True, B=True (XOR=False) -> el resultado debe ser False sin importar C
    assert evaluar_expresion_2(True, True, True) is False
    # A=True, B=False (XOR=True), C=True -> True∧True = True
    assert evaluar_expresion_2(True, False, True) is True
    # A=True, B=False (XOR=True), C=False -> True∧False = False
    assert evaluar_expresion_2(True, False, False) is False
    print("OK  test_expresion_2_xor_correcto")


# ---------------------------------------------------------------------------
# Caso 4: expresión 3 -> verifica específicamente el caso donde el
# código original tenía el bug (A=True, B=True, C=False)
# ---------------------------------------------------------------------------
def test_expresion_3_caso_del_bug_corregido():
    # (A∨B) = (T∨T) = True
    # (¬A∨C) = (F∨F) = False
    # Resultado correcto: True ∧ False = False
    # (el código original, con el bug, daba True en este caso)
    assert evaluar_expresion_3(True, True, False) is False
    print("OK  test_expresion_3_caso_del_bug_corregido")


# ---------------------------------------------------------------------------
# Caso 5: expresión 3 -> caso donde sí debe dar True
# ---------------------------------------------------------------------------
def test_expresion_3_resultado_verdadero():
    # A=False, B=True, C=True
    # (A∨B) = (F∨V) = True
    # (¬A∨C) = (V∨V) = True
    # Resultado: True ∧ True = True
    assert evaluar_expresion_3(False, True, True) is True
    print("OK  test_expresion_3_resultado_verdadero")


# ---------------------------------------------------------------------------
# Caso 6: la tabla de verdad completa tiene las 8 combinaciones esperadas
# ---------------------------------------------------------------------------
def test_tabla_verdad_tiene_8_filas():
    tabla = generar_tabla_verdad(evaluar_expresion_1)
    assert len(tabla) == 8

    combinaciones_esperadas = {
        (False, False, False), (False, False, True),
        (False, True, False), (False, True, True),
        (True, False, False), (True, False, True),
        (True, True, False), (True, True, True),
    }
    combinaciones_obtenidas = {(a, b, c) for a, b, c, _ in tabla}
    assert combinaciones_obtenidas == combinaciones_esperadas
    print("OK  test_tabla_verdad_tiene_8_filas")


# ---------------------------------------------------------------------------
# Ejecutor simple (sin depender de pytest)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_expresion_1_c_falso_domina()
    test_expresion_1_resultado_falso()
    test_expresion_2_xor_correcto()
    test_expresion_3_caso_del_bug_corregido()
    test_expresion_3_resultado_verdadero()
    test_tabla_verdad_tiene_8_filas()
    print("\nTodas las pruebas pasaron correctamente.")