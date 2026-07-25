"""
Pruebas del cierre de una estación (Punto 5)
===============================================

Cómo ejecutar:
    Desde la raíz del repositorio:
        python -m tests.test_5_cierre_estacion
    o bien, si se tiene pytest instalado:
        pytest tests/test_5_cierre_estacion.py -v
"""

import math
import sys
import os

RUTA_MODULO = os.path.join(
    os.path.dirname(__file__), "..", "src", "Grafos"
)
sys.path.insert(0, os.path.abspath(RUTA_MODULO))

from punto5_cierre_estacion import cerrar_vertice, cerrar_arista, calcular_impacto

# El módulo dijkstra.py ya quedó en sys.path al importar cierre_estacion.py
from dijkstra import Grafo, dijkstra, grafo_prueba


# ---------------------------------------------------------------------------
# Caso 1: cerrar un vértice elimina también sus aristas hacia otros vértices
# ---------------------------------------------------------------------------
def test_cerrar_vertice_elimina_sus_aristas():
    g = grafo_prueba()
    g_despues = cerrar_vertice(g, "Centro")

    assert "Centro" not in g_despues.adyacencia
    # Ningún vértice restante debe seguir apuntando a "Centro"
    for vecinos in g_despues.adyacencia.values():
        nombres_vecinos = [nombre for nombre, _ in vecinos]
        assert "Centro" not in nombres_vecinos
    print("OK  test_cerrar_vertice_elimina_sus_aristas")


# ---------------------------------------------------------------------------
# Caso 2: el grafo original no se modifica al cerrar un vértice (copia)
# ---------------------------------------------------------------------------
def test_grafo_original_no_se_modifica():
    g = grafo_prueba()
    vertices_antes = set(g.vertices())

    cerrar_vertice(g, "Centro")

    assert set(g.vertices()) == vertices_antes
    assert "Centro" in g.adyacencia
    print("OK  test_grafo_original_no_se_modifica")


# ---------------------------------------------------------------------------
# Caso 3: cerrar una arista específica solo afecta a esa conexión
# ---------------------------------------------------------------------------
def test_cerrar_arista_especifica():
    g = grafo_prueba()
    g_despues = cerrar_arista(g, "Museo", "Centro")

    vecinos_museo = [nombre for nombre, _ in g_despues.adyacencia["Museo"]]
    vecinos_centro = [nombre for nombre, _ in g_despues.adyacencia["Centro"]]

    assert "Centro" not in vecinos_museo
    assert "Museo" not in vecinos_centro
    # Otras conexiones de Museo deben seguir intactas
    assert "Calle26" in vecinos_museo
    print("OK  test_cerrar_arista_especifica")


# ---------------------------------------------------------------------------
# Caso 4: calcular_impacto detecta correctamente un aumento de distancia
# ---------------------------------------------------------------------------
def test_calcular_impacto_detecta_aumento():
    g_antes = grafo_prueba()
    g_despues = cerrar_vertice(g_antes, "Centro")

    filas = calcular_impacto(g_antes, g_despues, [("Universidad", "Terminal")])
    fila = filas[0]

    assert fila["distancia_antes"] == 9
    assert fila["distancia_despues"] > fila["distancia_antes"]
    assert fila["diferencia"] == fila["distancia_despues"] - fila["distancia_antes"]
    assert fila["estado"] == "AUMENTÓ"
    print("OK  test_calcular_impacto_detecta_aumento")


# ---------------------------------------------------------------------------
# Caso 5: calcular_impacto detecta correctamente cuando NO hay cambio
# ---------------------------------------------------------------------------
def test_calcular_impacto_detecta_sin_cambio():
    g_antes = grafo_prueba()
    g_despues = cerrar_vertice(g_antes, "Centro")

    filas = calcular_impacto(g_antes, g_despues, [("Portal", "Parque")])
    fila = filas[0]

    assert fila["diferencia"] == 0
    assert fila["estado"] == "SIN CAMBIO"
    print("OK  test_calcular_impacto_detecta_sin_cambio")


# ---------------------------------------------------------------------------
# Caso 6: calcular_impacto detecta correctamente una desconexión total
# ---------------------------------------------------------------------------
def test_calcular_impacto_detecta_desconexion():
    # Grafo pequeño con un único "puente" entre A y B
    g = Grafo()
    g.agregar_arista("A", "Puente", 1)
    g.agregar_arista("Puente", "B", 1)

    g_despues = cerrar_vertice(g, "Puente")

    filas = calcular_impacto(g, g_despues, [("A", "B")])
    fila = filas[0]

    assert fila["distancia_despues"] == math.inf
    assert fila["diferencia"] == math.inf
    assert fila["estado"] == "DESCONECTADO"
    print("OK  test_calcular_impacto_detecta_desconexion")


# ---------------------------------------------------------------------------
# Caso 7: se pueden procesar al menos cinco pares origen-destino a la vez
# ---------------------------------------------------------------------------
def test_procesa_multiples_pares():
    g_antes = grafo_prueba()
    g_despues = cerrar_vertice(g_antes, "Centro")

    pares = [
        ("Portal", "Estadio"),
        ("Portal", "Parque"),
        ("Universidad", "Terminal"),
        ("Calle26", "Estadio"),
        ("Museo", "Parque"),
    ]

    filas = calcular_impacto(g_antes, g_despues, pares)
    assert len(filas) == 5
    for fila in filas:
        assert fila["estado"] in ("AUMENTÓ", "SIN CAMBIO", "DESCONECTADO")
    print("OK  test_procesa_multiples_pares")


# ---------------------------------------------------------------------------
# Ejecutor simple (sin depender de pytest)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_cerrar_vertice_elimina_sus_aristas()
    test_grafo_original_no_se_modifica()
    test_cerrar_arista_especifica()
    test_calcular_impacto_detecta_aumento()
    test_calcular_impacto_detecta_sin_cambio()
    test_calcular_impacto_detecta_desconexion()
    test_procesa_multiples_pares()
    print("\nTodas las pruebas pasaron correctamente.")