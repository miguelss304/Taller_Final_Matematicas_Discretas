"""
Ruta más corta en una ciudad representada como grafo (Algoritmo de Dijkstra)
=============================================================================

El grafo puede cargarse de dos formas:
  1) Desde una estructura de datos definida en el código (función grafo_prueba()).
  2) Desde un archivo de texto con el formato:
         origen destino peso
     una arista por línea (ver función cargar_grafo_desde_archivo()).
     
"""

import heapq
import math


# ---------------------------------------------------------------------------
# 1. Estructura del grafo
# ---------------------------------------------------------------------------
class Grafo:
    """Grafo no dirigido ponderado, representado con listas de adyacencia."""

    def __init__(self):
        # dict: vertice -> lista de tuplas (vecino, peso)
        self.adyacencia = {}

    def agregar_vertice(self, v):
        if v not in self.adyacencia:
            self.adyacencia[v] = []

    def agregar_arista(self, u, v, peso, dirigido=False):
        if peso < 0:
            raise ValueError("Dijkstra requiere pesos no negativos.")
        self.agregar_vertice(u)
        self.agregar_vertice(v)
        self.adyacencia[u].append((v, peso))
        if not dirigido:
            self.adyacencia[v].append((u, peso))

    def vertices(self):
        return list(self.adyacencia.keys())


# ---------------------------------------------------------------------------
# 2. Carga del grafo desde archivo
# ---------------------------------------------------------------------------
def cargar_grafo_desde_archivo(ruta_archivo, dirigido=False):
    """
    Formato esperado del archivo (una arista por línea):
        Portal Calle26 5
        Calle26 Museo 3
        ...
    Las líneas vacías o que empiezan con '#' se ignoran.
    """
    g = Grafo()
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            partes = linea.split()
            if len(partes) != 3:
                raise ValueError(f"Línea con formato inválido: '{linea}'")
            u, v, peso = partes[0], partes[1], float(partes[2])
            g.agregar_arista(u, v, peso, dirigido=dirigido)
    return g


# ---------------------------------------------------------------------------
# 3. Grafo de prueba (8 vértices, 12 aristas) definido en código
# ---------------------------------------------------------------------------
def grafo_prueba():
    g = Grafo()
    aristas = [
        ("Portal",       "Calle26",     5),
        ("Portal",       "Terminal",    8),
        ("Calle26",      "Museo",       3),
        ("Calle26",      "Centro",      7),
        ("Museo",        "Centro",      2),
        ("Museo",        "Universidad", 6),
        ("Centro",       "Universidad", 4),
        ("Centro",       "Terminal",    5),
        ("Terminal",     "Estadio",     9),
        ("Universidad",  "Parque",      3),
        ("Parque",       "Estadio",     4),
        ("Estadio",      "Centro",      6),
    ]
    for u, v, peso in aristas:
        g.agregar_arista(u, v, peso)
    return g
    # 8 vértices: Portal, Calle26, Museo, Centro, Terminal,
    #             Universidad, Parque, Estadio
    # 12 aristas listadas arriba.


# ---------------------------------------------------------------------------
# 4. Algoritmo de Dijkstra
# ---------------------------------------------------------------------------
def dijkstra(grafo, origen, destino):
    """
    Devuelve (distancia_total, ruta) usando el algoritmo de Dijkstra.
    Si no existe camino, devuelve (math.inf, []).
    """
    if origen not in grafo.adyacencia:
        raise ValueError(f"El vértice de origen '{origen}' no existe en el grafo.")
    if destino not in grafo.adyacencia:
        raise ValueError(f"El vértice de destino '{destino}' no existe en el grafo.")

    distancias = {v: math.inf for v in grafo.vertices()}
    previos = {v: None for v in grafo.vertices()}
    distancias[origen] = 0

    # Cola de prioridad: (distancia_acumulada, vértice)
    cola = [(0, origen)]
    visitados = set()

    while cola:
        dist_actual, actual = heapq.heappop(cola)

        if actual in visitados:
            continue
        visitados.add(actual)

        if actual == destino:
            break

        for vecino, peso in grafo.adyacencia[actual]:
            if vecino in visitados:
                continue
            nueva_dist = dist_actual + peso
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                previos[vecino] = actual
                heapq.heappush(cola, (nueva_dist, vecino))

    if distancias[destino] == math.inf:
        return math.inf, []

    # Reconstruir la ruta siguiendo los "previos" desde destino hasta origen
    ruta = []
    nodo = destino
    while nodo is not None:
        ruta.append(nodo)
        nodo = previos[nodo]
    ruta.reverse()

    return distancias[destino], ruta


# ---------------------------------------------------------------------------
# 5. Programa principal / demostración por consola
# ---------------------------------------------------------------------------
def main():
    """Ejecución de ejemplo: pide origen y destino, o corre casos por defecto."""
    grafo = grafo_prueba()

    print("Vértices disponibles:", ", ".join(grafo.vertices()))
    print()

    pruebas = [
        ("Portal", "Estadio"),
        ("Portal", "Parque"),
        ("Universidad", "Terminal"),
    ]

    for origen, destino in pruebas:
        distancia, ruta = dijkstra(grafo, origen, destino)
        print(f"Ruta más corta de '{origen}' a '{destino}':")
        if ruta:
            print(f"  Camino:   {' -> '.join(ruta)}")
            print(f"  Distancia total: {distancia}")
        else:
            print("  No existe un camino entre esos vértices.")
        print()


if __name__ == "__main__":
    main()