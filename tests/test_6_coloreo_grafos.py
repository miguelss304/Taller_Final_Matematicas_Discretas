"""
Pruebas del coloreo de grafos (Punto 6)
===========================================
 
Cómo ejecutar:
    Desde la raíz del repositorio:
        python -m tests.test_6_coloreo_grafos
    o bien, si se tiene pytest instalado:
        pytest tests/test_6_coloreo_grafos.py -v
"""
 
import sys
import os
 
RUTA_MODULO = os.path.join(
    os.path.dirname(__file__), "..", "src", "Grafos"
)
sys.path.insert(0, os.path.abspath(RUTA_MODULO))
 
from punto6_coloreo_grafos import (
    grado,
    obtener_aristas,
    orden_grado_descendente,
    colorear_grafo_voraz,
    verificar_coloreo,
    num_colores,
    grafo_prueba,
)
 
# El módulo dijkstra.py ya quedó en sys.path al importar punto6_coloreo_grafos
from dijkstra import Grafo
 
 
# ---------------------------------------------------------------------------
# Caso 1: un triángulo (3 vértices mutuamente conectados) exige 3 colores
# ---------------------------------------------------------------------------
def test_triangulo_necesita_tres_colores():
    g = Grafo()
    g.agregar_arista("A", "B", 1)
    g.agregar_arista("B", "C", 1)
    g.agregar_arista("A", "C", 1)
 
    colores = colorear_grafo_voraz(g)
    valido, _ = verificar_coloreo(g, colores)
 
    assert valido
    assert num_colores(colores) == 3
    print("OK  test_triangulo_necesita_tres_colores")
 
 
# ---------------------------------------------------------------------------
# Caso 2: un orden de recorrido alternado puede desperdiciar colores
# ---------------------------------------------------------------------------
def test_orden_alternado_desperdicia_colores():
    g = _grafo_bipartito_de_prueba()
    orden_malo = ["A1", "B1", "A2", "B2", "A3", "B3"]
 
    colores = colorear_grafo_voraz(g, orden=orden_malo)
    valido, _ = verificar_coloreo(g, colores)
 
    assert valido
    assert num_colores(colores) == 3
    print("OK  test_orden_alternado_desperdicia_colores")
 
 
# ---------------------------------------------------------------------------
# Caso 3: agrupar el orden por partición alcanza el óptimo real
# ---------------------------------------------------------------------------
def test_orden_agrupado_alcanza_el_optimo():
    g = _grafo_bipartito_de_prueba()
    orden_bueno = ["A1", "A2", "A3", "B1", "B2", "B3"]
 
    colores = colorear_grafo_voraz(g, orden=orden_bueno)
    valido, _ = verificar_coloreo(g, colores)
 
    assert valido
    assert num_colores(colores) == 2
    print("OK  test_orden_agrupado_alcanza_el_optimo")
 
 
def _grafo_bipartito_de_prueba():
    """Grafo bipartito auxiliar: cada Ai se conecta con todos los Bj,
    salvo consigo mismo por índice. Óptimo teórico: 2 colores."""
    g = Grafo()
    conflictos = [
        ("A1", "B2"), ("A1", "B3"),
        ("A2", "B1"), ("A2", "B3"),
        ("A3", "B1"), ("A3", "B2"),
    ]
    for u, v in conflictos:
        g.agregar_arista(u, v, 1)
    return g
 
 
# ---------------------------------------------------------------------------
# Caso 4: verificar_coloreo() detecta un coloreo inválido armado a mano
# ---------------------------------------------------------------------------
def test_verificar_coloreo_detecta_conflicto():
    g = Grafo()
    g.agregar_arista("X", "Y", 1)
 
    coloreo_malo = {"X": 0, "Y": 0}
    valido, conflictos = verificar_coloreo(g, coloreo_malo)
 
    assert not valido
    assert conflictos == [("X", "Y")]
    print("OK  test_verificar_coloreo_detecta_conflicto")
 
 
# ---------------------------------------------------------------------------
# Caso 5: grado() cuenta correctamente los vecinos de un vértice
# ---------------------------------------------------------------------------
def test_grado_cuenta_vecinos_correctamente():
    g = Grafo()
    g.agregar_arista("Uno", "Dos", 1)
    g.agregar_arista("Uno", "Tres", 1)
 
    assert grado(g, "Uno") == 2
    assert grado(g, "Dos") == 1
    print("OK  test_grado_cuenta_vecinos_correctamente")
 
 
# ---------------------------------------------------------------------------
# Caso 6: obtener_aristas() no duplica una conexión no dirigida
# ---------------------------------------------------------------------------
def test_obtener_aristas_sin_duplicados():
    g = Grafo()
    g.agregar_arista("Uno", "Dos", 1)
    g.agregar_arista("Uno", "Tres", 1)
 
    aristas = obtener_aristas(g)
 
    assert len(aristas) == 2
    print("OK  test_obtener_aristas_sin_duplicados")
 
 
# ---------------------------------------------------------------------------
# Caso 7: el grafo de prueba cumple el mínimo de 10 vértices del enunciado
# ---------------------------------------------------------------------------
def test_grafo_prueba_cumple_minimo_diez_vertices():
    g = grafo_prueba()
    assert len(g.vertices()) >= 10
    print("OK  test_grafo_prueba_cumple_minimo_diez_vertices")
 
 
# ---------------------------------------------------------------------------
# Caso 8: el grafo de prueba produce un coloreo válido con 3 colores
# ---------------------------------------------------------------------------
def test_grafo_prueba_da_coloreo_valido_con_tres_colores():
    g = grafo_prueba()
    orden = orden_grado_descendente(g)
    colores = colorear_grafo_voraz(g, orden=orden)
    valido, _ = verificar_coloreo(g, colores)
 
    assert valido
    assert num_colores(colores) == 3
    print("OK  test_grafo_prueba_da_coloreo_valido_con_tres_colores")
 
 
# ---------------------------------------------------------------------------
# Ejecutor simple (sin depender de pytest)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_triangulo_necesita_tres_colores()
    test_orden_alternado_desperdicia_colores()
    test_orden_agrupado_alcanza_el_optimo()
    test_verificar_coloreo_detecta_conflicto()
    test_grado_cuenta_vecinos_correctamente()
    test_obtener_aristas_sin_duplicados()
    test_grafo_prueba_cumple_minimo_diez_vertices()
    test_grafo_prueba_da_coloreo_valido_con_tres_colores()
    print("\nTodas las pruebas pasaron correctamente.")