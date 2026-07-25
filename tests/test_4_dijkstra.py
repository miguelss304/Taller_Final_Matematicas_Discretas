"""
Pruebas del algoritmo de Dijkstra (Punto 4 - Ruta más corta en una ciudad)
============================================================================

Cómo ejecutar:
    Desde la raíz del repositorio:
        python -m tests.test_4_dijkstra
    o bien, si se tiene pytest instalado:
        pytest tests/test_4_dijkstra.py -v

Cada función test_* verifica un caso de entrada/salida distinto:
distancia y ruta esperadas, vértice aislado, vértice inexistente,
peso negativo, y carga desde archivo.
"""

import math
import sys
import os

# Permite importar el módulo dijkstra.py aunque el test se corra desde la
# raíz del repositorio. Se apunta directo a la carpeta que lo contiene
# (src/Grafos/Punto 4 Taller MD) en vez de importarlo como paquete, ya
# que el nombre de la carpeta tiene espacios.
RUTA_MODULO = os.path.join(
    os.path.dirname(__file__), "..", "src", "Grafos", "punto4_dijkstra"
)
sys.path.insert(0, os.path.abspath(RUTA_MODULO))

from dijkstra import Grafo, dijkstra, grafo_prueba, cargar_grafo_desde_archivo


# ---------------------------------------------------------------------------
# Caso 1: ruta más corta esperada entre dos vértices conocidos
# ---------------------------------------------------------------------------
def test_ruta_portal_estadio():
    g = grafo_prueba()
    distancia, ruta = dijkstra(g, "Portal", "Estadio")

    # Entrada: grafo de prueba, origen="Portal", destino="Estadio"
    # Salida esperada: distancia=16, camino Portal-Calle26-Museo-Centro-Estadio
    assert distancia == 16
    assert ruta == ["Portal", "Calle26", "Museo", "Centro", "Estadio"]
    print("OK  test_ruta_portal_estadio")


# ---------------------------------------------------------------------------
# Caso 2: otra pareja origen-destino, ruta distinta
# ---------------------------------------------------------------------------
def test_ruta_universidad_terminal():
    g = grafo_prueba()
    distancia, ruta = dijkstra(g, "Universidad", "Terminal")

    # Entrada: origen="Universidad", destino="Terminal"
    # Salida esperada: distancia=9, camino Universidad-Centro-Terminal
    assert distancia == 9
    assert ruta == ["Universidad", "Centro", "Terminal"]
    print("OK  test_ruta_universidad_terminal")


# ---------------------------------------------------------------------------
# Caso 3: origen igual a destino -> distancia 0, ruta de un solo vértice
# ---------------------------------------------------------------------------
def test_origen_igual_destino():
    g = grafo_prueba()
    distancia, ruta = dijkstra(g, "Museo", "Museo")

    # Entrada: origen="Museo", destino="Museo"
    # Salida esperada: distancia=0, ruta=["Museo"]
    assert distancia == 0
    assert ruta == ["Museo"]
    print("OK  test_origen_igual_destino")


# ---------------------------------------------------------------------------
# Caso 4: vértice desconectado del resto del grafo -> no existe camino
# ---------------------------------------------------------------------------
def test_vertice_desconectado():
    g = grafo_prueba()
    g.agregar_vertice("Aeropuerto")  # vértice sin aristas

    distancia, ruta = dijkstra(g, "Portal", "Aeropuerto")

    # Entrada: destino sin conexión alguna
    # Salida esperada: distancia=inf, ruta=[]
    assert distancia == math.inf
    assert ruta == []
    print("OK  test_vertice_desconectado")


# ---------------------------------------------------------------------------
# Caso 5: vértice que no existe en el grafo -> debe lanzar ValueError
# ---------------------------------------------------------------------------
def test_vertice_inexistente():
    g = grafo_prueba()
    try:
        dijkstra(g, "Portal", "NoExiste")
        assert False, "Se esperaba un ValueError"
    except ValueError:
        print("OK  test_vertice_inexistente")


# ---------------------------------------------------------------------------
# Caso 6: peso negativo -> debe lanzar ValueError al construir el grafo
# ---------------------------------------------------------------------------
def test_peso_negativo_rechazado():
    g = Grafo()
    try:
        g.agregar_arista("A", "B", -3)
        assert False, "Se esperaba un ValueError por peso negativo"
    except ValueError:
        print("OK  test_peso_negativo_rechazado")


# ---------------------------------------------------------------------------
# Caso 7: carga del grafo desde archivo de texto y verificación cruzada
# ---------------------------------------------------------------------------
def test_carga_desde_archivo():
    ruta_archivo = os.path.join(
        os.path.dirname(__file__), "..", "src", "Grafos", "punto4_dijkstra",
        "grafo_ciudad.txt"
    )
    g_archivo = cargar_grafo_desde_archivo(ruta_archivo)
    g_codigo = grafo_prueba()

    # El grafo cargado desde archivo debe dar el mismo resultado
    # que el grafo definido directamente en código.
    dist_archivo, ruta_a = dijkstra(g_archivo, "Portal", "Estadio")
    dist_codigo, ruta_c = dijkstra(g_codigo, "Portal", "Estadio")

    assert dist_archivo == dist_codigo == 16
    assert ruta_a == ruta_c
    print("OK  test_carga_desde_archivo")


# ---------------------------------------------------------------------------
# Ejecutor simple (sin depender de pytest)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    test_ruta_portal_estadio()
    test_ruta_universidad_terminal()
    test_origen_igual_destino()
    test_vertice_desconectado()
    test_vertice_inexistente()
    test_peso_negativo_rechazado()
    test_carga_desde_archivo()
    print("\nTodas las pruebas pasaron correctamente.")