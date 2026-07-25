"""
Ejecuta Dijkstra sobre un grafo cargado desde un archivo externo.

Uso:
    python3 ejecutar_grafo.py <archivo_grafo.txt> <origen> <destino>

Ejemplo:
    python3 ejecutar_grafo.py mi_ciudad.txt CasaA Trabajo

El archivo debe tener el mismo formato que grafo_ciudad.txt:
    origen destino peso
    (una arista por línea, líneas vacías o con '#' se ignoran)
"""

import sys
from dijkstra import cargar_grafo_desde_archivo, dijkstra


def main():
    if len(sys.argv) != 4:
        print("Uso: python3 ejecutar_grafo.py <archivo.txt> <origen> <destino>")
        sys.exit(1)

    archivo, origen, destino = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        grafo = cargar_grafo_desde_archivo(archivo)
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{archivo}'.")
        sys.exit(1)

    print(f"Grafo cargado. Vértices: {', '.join(grafo.vertices())}\n")

    try:
        distancia, ruta = dijkstra(grafo, origen, destino)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if ruta:
        print(f"Ruta más corta de '{origen}' a '{destino}':")
        print(f"  Camino:   {' -> '.join(ruta)}")
        print(f"  Distancia total: {distancia}")
    else:
        print(f"No existe un camino entre '{origen}' y '{destino}'.")


if __name__ == "__main__":
    main()