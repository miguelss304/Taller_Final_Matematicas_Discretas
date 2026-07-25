"""
Pruebas de la simplificación booleana (Punto 8)
==================================================
 
Cómo ejecutar:
    Desde la raíz del repositorio:
        python -m tests.test_8_simplificacion_booleana
    o bien, si se tiene pytest instalado:
        pytest tests/test_8_simplificacion_booleana.py -v
 
Se prueban tanto las funciones internas del algoritmo de Quine-McCluskey
(combinación de términos, obtención de implicantes primos, selección de
cobertura, traducción a expresión) como el resultado final de
`simplificar`, verificando que la expresión obtenida sea equivalente a
la función original.
"""
 
import sys
import os
 
RUTA_MODULO = os.path.join(
    os.path.dirname(__file__), "..", "src", "Bool"
)
sys.path.insert(0, os.path.abspath(RUTA_MODULO))
 
from punto8_simplificacion_booleana import (
    a_binario,
    combinar_terminos,
    obtener_implicantes_primos,
    seleccionar_implicantes,
    termino_a_expresion,
    verificar_equivalencia,
    simplificar,
)
 
 
# ---------------------------------------------------------------------------
# Caso 1: ejemplo obligatorio del taller
# ---------------------------------------------------------------------------
def test_caso_obligatorio_taller():
    # Entrada: minterminos={1,3,5,7}, variables=A,B,C
    # Salida esperada: expresión equivalente a C
    resultado = simplificar([1, 3, 5, 7], 3, ['A', 'B', 'C'])
    assert resultado['expresion'] == 'C'
    assert resultado['equivalente'] is True
    print("OK  test_caso_obligatorio_taller")
 
 
# ---------------------------------------------------------------------------
# Caso 2: conversión de mintermino decimal a binario
# ---------------------------------------------------------------------------
def test_a_binario_convierte_correctamente():
    assert a_binario(5, 3) == '101'
    assert a_binario(0, 4) == '0000'
    assert a_binario(15, 4) == '1111'
    print("OK  test_a_binario_convierte_correctamente")
 
 
# ---------------------------------------------------------------------------
# Caso 3: dos términos que difieren en un solo bit se combinan
# ---------------------------------------------------------------------------
def test_combinar_terminos_un_bit_de_diferencia():
    # '101' y '111' difieren solo en la posición del medio
    resultado = combinar_terminos('101', '111')
    assert resultado == '1-1'
    print("OK  test_combinar_terminos_un_bit_de_diferencia")
 
 
# ---------------------------------------------------------------------------
# Caso 4: términos que difieren en más de un bit no se combinan
# ---------------------------------------------------------------------------
def test_combinar_terminos_mas_de_un_bit_no_combina():
    resultado = combinar_terminos('100', '111')
    assert resultado is None
    print("OK  test_combinar_terminos_mas_de_un_bit_no_combina")
 
 
# ---------------------------------------------------------------------------
# Caso 5: los guiones deben estar alineados para poder combinar
# ---------------------------------------------------------------------------
def test_combinar_terminos_respeta_guiones_alineados():
    # Guion en la misma posición en ambos términos: sí se combinan
    resultado = combinar_terminos('1-0', '1-1')
    assert resultado == '1--'
    # Guion en posiciones distintas: no se combinan (cuenta como diferencia)
    resultado_invalido = combinar_terminos('1-0', '-10')
    assert resultado_invalido is None
    print("OK  test_combinar_terminos_respeta_guiones_alineados")
 
 
# ---------------------------------------------------------------------------
# Caso 6: un solo mintermino no se puede simplificar
# ---------------------------------------------------------------------------
def test_implicantes_primos_caso_minimo():
    # Sin nada con qué combinarse, el implicante primo es el término
    # completo, sin ningún guion.
    implicantes = obtener_implicantes_primos([5], 3)
    assert implicantes == {('101', frozenset({5}))}
    print("OK  test_implicantes_primos_caso_minimo")
 
 
# ---------------------------------------------------------------------------
# Caso 7: el único implicante primo queda seleccionado como esencial
# ---------------------------------------------------------------------------
def test_seleccionar_implicantes_encuentra_esenciales():
    implicantes = obtener_implicantes_primos([1, 3, 5, 7], 3)
    seleccionados = seleccionar_implicantes(implicantes, [1, 3, 5, 7])
    assert seleccionados == {('--1', frozenset({1, 3, 5, 7}))}
    print("OK  test_seleccionar_implicantes_encuentra_esenciales")
 
 
# ---------------------------------------------------------------------------
# Caso 8: traducción de bits a literales (normal, negado, omitido)
# ---------------------------------------------------------------------------
def test_termino_a_expresion_traduce_bits():
    assert termino_a_expresion('101', ['A', 'B', 'C']) == "AB'C"
    assert termino_a_expresion('--1', ['A', 'B', 'C']) == "C"
    assert termino_a_expresion('---', ['A', 'B', 'C']) == "1"
    print("OK  test_termino_a_expresion_traduce_bits")
 
 
# ---------------------------------------------------------------------------
# Caso 9: la verificación detecta una expresión que no corresponde
# ---------------------------------------------------------------------------
def test_verificar_equivalencia_detecta_expresion_incorrecta():
    # '000' cubre el mintermino 0, que no pertenece a la función
    # {1,3,5,7}; la verificación debe encontrar la discrepancia.
    implicante_incorrecto = {('000', frozenset({0}))}
    equivalente, fallo = verificar_equivalencia(
        [1, 3, 5, 7], implicante_incorrecto, 3, ['A', 'B', 'C']
    )
    assert equivalente is False
    assert fallo == 0
    print("OK  test_verificar_equivalencia_detecta_expresion_incorrecta")
 
 
# ---------------------------------------------------------------------------
# Caso 10: función de 4 variables que requiere el paso de cobertura
# (varios implicantes primos, no solo esenciales)
# ---------------------------------------------------------------------------
def test_simplificar_caso_con_cobertura_no_trivial():
    minterminos = [0, 1, 2, 5, 6, 7, 8, 9, 10, 14]
    resultado = simplificar(minterminos, 4, ['A', 'B', 'C', 'D'])
    assert resultado['equivalente'] is True
    # La expresión esperada tiene 3 términos (2 símbolos '+')
    assert resultado['expresion'].count('+') == 2
    print("OK  test_simplificar_caso_con_cobertura_no_trivial")
 
 
# ---------------------------------------------------------------------------
# Caso 11: función que vale 1 en todo el espacio colapsa a la constante 1
# ---------------------------------------------------------------------------
def test_funcion_que_cubre_todo_el_espacio():
    todos_los_minterminos = list(range(2 ** 3))  # 0..7, para A,B,C
    resultado = simplificar(todos_los_minterminos, 3, ['A', 'B', 'C'])
    assert resultado['expresion'] == '1'
    assert resultado['equivalente'] is True
    print("OK  test_funcion_que_cubre_todo_el_espacio")
 
 
# ---------------------------------------------------------------------------
# Ejecutor simple (sin depender de pytest)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_caso_obligatorio_taller()
    test_a_binario_convierte_correctamente()
    test_combinar_terminos_un_bit_de_diferencia()
    test_combinar_terminos_mas_de_un_bit_no_combina()
    test_combinar_terminos_respeta_guiones_alineados()
    test_implicantes_primos_caso_minimo()
    test_seleccionar_implicantes_encuentra_esenciales()
    test_termino_a_expresion_traduce_bits()
    test_verificar_equivalencia_detecta_expresion_incorrecta()
    test_simplificar_caso_con_cobertura_no_trivial()
    test_funcion_que_cubre_todo_el_espacio()
    print("\nTodas las pruebas pasaron correctamente.")
