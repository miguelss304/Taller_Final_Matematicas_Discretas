"""
Pruebas del cifrado César (Punto 1)
=====================================

Cómo ejecutar:
    Desde la raíz del repositorio:
        python -m tests.test_1_cesar
    o bien, si se tiene pytest instalado:
        pytest tests/test_1_cesar.py -v

Se prueban las funciones puras (cifrar_texto, descifrar_texto), que no
dependen de input(), para poder verificar entradas y salidas exactas.
"""

import sys
import os

# Apunta a la carpeta que contiene cesar.py (nombre con espacios, por eso
# se importa el módulo directo en vez de como paquete).
RUTA_MODULO = os.path.join(
    os.path.dirname(__file__), "..", "src", "Criptografia"
)
sys.path.insert(0, os.path.abspath(RUTA_MODULO))

from punto1_cesar import cifrar_texto, descifrar_texto, construir_tabla


# ---------------------------------------------------------------------------
# Caso 1: cifrado del ejemplo dado en el enunciado del taller
# ---------------------------------------------------------------------------
def test_cifrado_ejemplo_taller():
    # Entrada: texto="HOLA UNAL", k=3
    # Salida esperada: "KROD XQDO"
    resultado = cifrar_texto("HOLA UNAL", 3)
    assert resultado == "KROD XQDO"
    print("OK  test_cifrado_ejemplo_taller")


# ---------------------------------------------------------------------------
# Caso 2: descifrado inverso del ejemplo anterior
# ---------------------------------------------------------------------------
def test_descifrado_ejemplo_taller():
    # Entrada: texto="KROD XQDO", k=3
    # Salida esperada: "HOLA UNAL"
    resultado = descifrar_texto("KROD XQDO", 3)
    assert resultado == "HOLA UNAL"
    print("OK  test_descifrado_ejemplo_taller")


# ---------------------------------------------------------------------------
# Caso 3: el texto debe conservar espacios, números y signos de puntuación
# ---------------------------------------------------------------------------
def test_conserva_caracteres_no_alfabeticos():
    # Entrada: texto con números y signos, k=1
    # Solo las letras cambian; el resto queda intacto.
    resultado = cifrar_texto("HOLA, MUNDO 123!", 1)
    assert resultado == "IPMB, NVOEP 123!"
    print("OK  test_conserva_caracteres_no_alfabeticos")


# ---------------------------------------------------------------------------
# Caso 4: desplazamiento k=0 no debe alterar el texto
# ---------------------------------------------------------------------------
def test_desplazamiento_cero():
    # Entrada: k=0 -> el texto cifrado debe ser idéntico al original
    resultado = cifrar_texto("PRUEBA", 0)
    assert resultado == "PRUEBA"
    print("OK  test_desplazamiento_cero")


# ---------------------------------------------------------------------------
# Caso 5: desplazamiento que da la vuelta al alfabeto (Z + 1 = A)
# ---------------------------------------------------------------------------
def test_desplazamiento_da_la_vuelta():
    # Entrada: texto="XYZ", k=3 -> X+3=A, Y+3=B, Z+3=C
    resultado = cifrar_texto("XYZ", 3)
    assert resultado == "ABC"
    print("OK  test_desplazamiento_da_la_vuelta")


# ---------------------------------------------------------------------------
# Caso 6: cifrar y luego descifrar con el mismo k regresa el texto original
# ---------------------------------------------------------------------------
def test_cifrar_y_descifrar_es_identidad():
    original = "ESTE ES UN MENSAJE DE PRUEBA"
    k = 11
    cifrado = cifrar_texto(original, k)
    descifrado = descifrar_texto(cifrado, k)
    assert descifrado == original
    print("OK  test_cifrar_y_descifrar_es_identidad")


# ---------------------------------------------------------------------------
# Caso 7: la tabla de sustitución tiene las 26 letras y es una permutación
# ---------------------------------------------------------------------------
def test_tabla_es_permutacion_valida():
    tabla = construir_tabla(5, direccion=1)
    assert len(tabla) == 26
    assert set(tabla.values()) == set(tabla.keys())  # misma cantidad de letras, sin repetidos
    print("OK  test_tabla_es_permutacion_valida")


# ---------------------------------------------------------------------------
# Ejecutor simple (sin depender de pytest)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_cifrado_ejemplo_taller()
    test_descifrado_ejemplo_taller()
    test_conserva_caracteres_no_alfabeticos()
    test_desplazamiento_cero()
    test_desplazamiento_da_la_vuelta()
    test_cifrar_y_descifrar_es_identidad()
    test_tabla_es_permutacion_valida()
    print("\nTodas las pruebas pasaron correctamente.")