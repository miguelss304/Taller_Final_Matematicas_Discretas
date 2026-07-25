"""
Cierre de una estación: medir el impacto en la red
=====================================================

Reutiliza el grafo y el algoritmo de Dijkstra del Punto 4. Simula el
cierre de un vértice (estación) o de una arista (conexión), y compara
las rutas más cortas entre varios pares origen-destino antes y después
del cierre, para medir qué tanto se afecta la red.

Estructura del archivo:
    1. Importación del grafo y Dijkstra ya implementados (Punto 4).
    2. Funciones para simular el cierre de un vértice o de una arista.
    3. Función que calcula el impacto sobre una lista de pares origen-destino.
    4. Función que arma e imprime la tabla de resultados.
    5. Programa principal (caso de prueba con el grafo de la ciudad).
"""

import copy
import math
import sys
import os

# Importa el módulo dijkstra.py desde la carpeta del Punto 4, reutilizando
# la misma implementación de Grafo y del algoritmo, en vez de duplicarla.
RUTA_PUNTO_4 = os.path.join(os.path.dirname(__file__), "punto4_dijkstra")
sys.path.insert(0, os.path.abspath(RUTA_PUNTO_4))

from dijkstra import Grafo, dijkstra, grafo_prueba


# ---------------------------------------------------------------------------
# 2. Simulación del cierre de un vértice o de una arista
# ---------------------------------------------------------------------------
def cerrar_vertice(grafo, vertice):
    """
    Devuelve una copia del grafo sin el vértice indicado (y sin ninguna
    arista que llegue o salga de él). El grafo original no se modifica.
    """
    nuevo_grafo = copy.deepcopy(grafo)

    if vertice not in nuevo_grafo.adyacencia:
        raise ValueError(f"El vértice '{vertice}' no existe en el grafo.")

    # Elimina el vértice y su lista de adyacencia
    del nuevo_grafo.adyacencia[vertice]

    # Elimina cualquier arista que otros vértices tuvieran hacia el cerrado
    for v in nuevo_grafo.adyacencia:
        nuevo_grafo.adyacencia[v] = [
            (vecino, peso) for vecino, peso in nuevo_grafo.adyacencia[v]
            if vecino != vertice
        ]

    return nuevo_grafo


def cerrar_arista(grafo, u, v):
    """
    Devuelve una copia del grafo sin la arista (u, v) en ninguno de los
    dos sentidos (el grafo de prueba es no dirigido). El grafo original
    no se modifica.
    """
    nuevo_grafo = copy.deepcopy(grafo)

    if u not in nuevo_grafo.adyacencia or v not in nuevo_grafo.adyacencia:
        raise ValueError(f"El vértice '{u}' o '{v}' no existe en el grafo.")

    nuevo_grafo.adyacencia[u] = [
        (vecino, peso) for vecino, peso in nuevo_grafo.adyacencia[u] if vecino != v
    ]
    nuevo_grafo.adyacencia[v] = [
        (vecino, peso) for vecino, peso in nuevo_grafo.adyacencia[v] if vecino != u
    ]

    return nuevo_grafo


# ---------------------------------------------------------------------------
# 3. Cálculo del impacto sobre una lista de pares origen-destino
# ---------------------------------------------------------------------------
def calcular_impacto(grafo_antes, grafo_despues, pares):
    """
    Para cada par (origen, destino) en `pares`, calcula la distancia más
    corta antes y después del cierre, y determina el estado del cambio.

    Devuelve una lista de diccionarios con las columnas:
        origen, destino, distancia_antes, distancia_despues,
        diferencia, estado
    """
    filas = []

    for origen, destino in pares:
        dist_antes, _ = dijkstra(grafo_antes, origen, destino)

        # Si alguno de los dos vértices ya no existe en el grafo tras el
        # cierre (porque era justo el vértice cerrado), se considera
        # directamente desconectado.
        if origen not in grafo_despues.adyacencia or destino not in grafo_despues.adyacencia:
            dist_despues = math.inf
        else:
            dist_despues, _ = dijkstra(grafo_despues, origen, destino)

        if dist_despues == math.inf:
            diferencia = math.inf
            estado = "DESCONECTADO"
        else:
            diferencia = dist_despues - dist_antes
            estado = "AUMENTÓ" if diferencia > 0 else "SIN CAMBIO"

        filas.append({
            "origen": origen,
            "destino": destino,
            "distancia_antes": dist_antes,
            "distancia_despues": dist_despues,
            "diferencia": diferencia,
            "estado": estado,
        })

    return filas


# ---------------------------------------------------------------------------
# 4. Presentación de resultados como tabla
# ---------------------------------------------------------------------------
def imprimir_tabla(filas):
    """Imprime la lista de resultados de calcular_impacto en forma de tabla."""
    encabezado = f"{'Origen':<12}{'Destino':<12}{'Antes':<10}{'Después':<10}{'Diferencia':<12}{'Estado':<15}"
    print(encabezado)
    print("-" * len(encabezado))

    for fila in filas:
        antes = fila["distancia_antes"]
        despues = fila["distancia_despues"]
        diferencia = fila["diferencia"]

        despues_str = "inf" if despues == math.inf else str(despues)
        diferencia_str = "inf" if diferencia == math.inf else str(diferencia)

        print(
            f"{fila['origen']:<12}{fila['destino']:<12}{antes:<10}"
            f"{despues_str:<10}{diferencia_str:<12}{fila['estado']:<15}"
        )


# ---------------------------------------------------------------------------
# 5. Programa principal
# ---------------------------------------------------------------------------
def main():
    grafo_antes = grafo_prueba()

    # Se simula el cierre del vértice "Centro": es el punto con más
    # conexiones del grafo de prueba (Calle26, Museo, Universidad,
    # Terminal, Estadio), por lo que su cierre debería tener un impacto
    # notorio sobre varias rutas.
    vertice_cerrado = "Centro"
    grafo_despues = cerrar_vertice(grafo_antes, vertice_cerrado)

    pares = [
        ("Portal", "Estadio"),
        ("Portal", "Parque"),
        ("Universidad", "Terminal"),
        ("Calle26", "Estadio"),
        ("Museo", "Parque"),
    ]

    print(f"Simulando el cierre del vértice: '{vertice_cerrado}'\n")

    filas = calcular_impacto(grafo_antes, grafo_despues, pares)
    imprimir_tabla(filas)


if __name__ == "__main__":
    main()