"""
Coloreo de grafos: organizar exámenes sin choques (Punto 6)
=====================================================================

Reutiliza la clase Grafo ya implementada en el Punto 4 (dijkstra.py) en
vez de duplicarla. El coloreo no necesita distancias, así que cada
conflicto entre cursos se agrega como una arista de peso 1; el peso
simplemente se ignora en todo lo que sigue.

Estructura del archivo:
    1. Importación de la clase Grafo ya implementada (Punto 4).
    2. Grafo de prueba: cursos (vértices) y conflictos (aristas),
       definido directamente en código.
    3. Carga alternativa del grafo desde un archivo de texto.
    4. Funciones auxiliares sobre la estructura de adyacencia
       (grado de un vértice, lista de aristas únicas).
    5. Heurística de orden Welsh-Powell (mayor a menor grado).
    6. Algoritmo voraz de coloreo.
    7. Verificación de que ningún par de vértices adyacentes
       comparta color.
    8. Presentación de resultados como tabla.
    9. Programa principal (caso de prueba con el grafo de cursos).
"""

import sys
import os

# Importa el módulo dijkstra.py desde la carpeta del Punto 4, reutilizando
# la misma clase Grafo en vez de duplicarla. Este archivo vive ahora en
# src/Grafos/punto6_coloreo_grafos/, así que hay que subir un nivel (..)
# antes de bajar a punto4_dijkstra/.
RUTA_PUNTO_4 = os.path.join(os.path.dirname(__file__), "..", "punto4_dijkstra")
sys.path.insert(0, os.path.abspath(RUTA_PUNTO_4))

from dijkstra import Grafo


# ---------------------------------------------------------------------------
# 2. Grafo de prueba (12 vértices / cursos, 18 aristas / conflictos)
# ---------------------------------------------------------------------------
def grafo_prueba():
    g = Grafo()
    conflictos = [
        ("BasesDeDatos",      "FEM"),
        ("BasesDeDatos",      "ProgramacionI"),
        ("BasesDeDatos",      "IngSoftware"),
        ("BasesDeDatos",      "Quimica"),
        ("FEM",               "Calculo"),
        ("FEM",               "Fisica2"),
        ("FEM",               "SistemasOperativos"),
        ("Discreta",          "ProgramacionI"),
        ("Discreta",          "Algebra"),
        ("Discreta",          "Estadistica"),
        ("Calculo",           "Algebra"),
        ("Calculo",           "Fisica2"),
        ("ProgramacionI",     "IngSoftware"),
        ("ProgramacionI",     "SistemasOperativos"),
        ("IngSoftware",       "RedesComputadores"),
        ("Fisica2",           "Quimica"),
        ("Algebra",           "Estadistica"),
        ("RedesComputadores", "SistemasOperativos"),
    ]
    for u, v in conflictos:
        # El peso es obligatorio en agregar_arista() del Punto 4, pero
        # para el coloreo no tiene ningún significado: solo importa que
        # la arista exista.
        g.agregar_arista(u, v, peso=1)
    return g
    # 12 vértices: BasesDeDatos, FEM, ProgramacionI, IngSoftware, Discreta,
    #              Algebra, Calculo, Fisica2, SistemasOperativos,
    #              RedesComputadores, Quimica, Estadistica
    # 18 aristas listadas arriba.


# ---------------------------------------------------------------------------
# 3. Carga alternativa del grafo desde un archivo de texto
# ---------------------------------------------------------------------------
def cargar_grafo_desde_archivo(ruta_archivo):
    """
    Formato esperado del archivo (un conflicto por línea):
        BasesDeDatos FEM
        FEM Calculo
        ...
    Las líneas vacías o que empiezan con '#' se ignoran.

    A diferencia del cargador del Punto 4 (que exige 3 columnas porque
    Dijkstra sí necesita un peso), aquí solo se piden 2 columnas: el
    coloreo no usa distancias, solo necesita saber que el conflicto
    existe. Igual que en grafo_prueba(), se agrega un peso de relleno
    (peso=1) porque la clase Grafo del Punto 4 lo exige, pero ese valor
    no se usa en ninguna función de este archivo.
    """
    g = Grafo()
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            partes = linea.split()
            if len(partes) != 2:
                raise ValueError(f"Línea con formato inválido: '{linea}'")
            u, v = partes[0], partes[1]
            g.agregar_arista(u, v, peso=1)
    return g


# ---------------------------------------------------------------------------
# 4. Funciones auxiliares sobre la estructura de adyacencia
# ---------------------------------------------------------------------------
def grado(grafo, v):
    """Número de vecinos de v (la clase Grafo del Punto 4 no expone esto)."""
    return len(grafo.adyacencia[v])


def obtener_aristas(grafo):
    """
    Devuelve la lista de aristas únicas como tuplas (u, v), leyendo la
    adyacencia (vecino, peso) del Grafo del Punto 4 e ignorando el peso.
    """
    vistas = set()
    lista = []
    for u in grafo.adyacencia:
        for vecino, _peso in grafo.adyacencia[u]:
            par = tuple(sorted((u, vecino)))
            if par not in vistas:
                vistas.add(par)
                lista.append(par)
    return lista


# ---------------------------------------------------------------------------
# 5. Orden de recorrido: Welsh-Powell (mayor a menor grado)
# ---------------------------------------------------------------------------
def orden_grado_descendente(grafo):
    """
    Ordena los vértices de mayor a menor grado. En caso de empate se usa
    el nombre para tener un resultado determinista. Colorear primero los
    vértices más conectados suele reducir el número de colores usados
    frente a un orden arbitrario.
    """
    return sorted(grafo.vertices(), key=lambda v: (-grado(grafo, v), v))


# ---------------------------------------------------------------------------
# 6. Algoritmo voraz de coloreo
# ---------------------------------------------------------------------------
def colorear_grafo_voraz(grafo, orden=None):
    """
    Asigna un color (entero 0, 1, 2, ...) a cada vértice siguiendo el
    orden dado, de forma que ningún vértice comparta color con un
    vecino ya coloreado. Si `orden` es None, se usa el orden de
    inserción del grafo.

    Devuelve un dict: vertice -> color.
    """
    if orden is None:
        orden = grafo.vertices()

    colores = {}
    for v in orden:
        colores_vecinos = {
            colores[vecino]
            for vecino, _peso in grafo.adyacencia[v]
            if vecino in colores
        }
        color = 0
        while color in colores_vecinos:
            color += 1
        colores[v] = color

    return colores


# ---------------------------------------------------------------------------
# 7. Verificación de validez del coloreo
# ---------------------------------------------------------------------------
def verificar_coloreo(grafo, colores):
    """
    Revisa todas las aristas del grafo y confirma que ningún par de
    vértices adyacentes comparta color.

    Devuelve (es_valido, lista_de_conflictos).
    """
    conflictos = []
    for u, v in obtener_aristas(grafo):
        if colores[u] == colores[v]:
            conflictos.append((u, v))
    return len(conflictos) == 0, conflictos


# ---------------------------------------------------------------------------
# 8. Presentación de resultados como tabla
# ---------------------------------------------------------------------------
def num_colores(colores):
    return max(colores.values()) + 1 if colores else 0


def imprimir_tabla(grafo, colores):
    """Imprime cada curso con su grado, color asignado y franja horaria."""
    encabezado = f"{'Curso':<20}{'Grado':<8}{'Color':<8}{'Franja':<12}"
    print(encabezado)
    print("-" * len(encabezado))

    for v in sorted(colores, key=lambda x: (colores[x], x)):
        c = colores[v]
        print(f"{v:<20}{grado(grafo, v):<8}{c:<8}{'Franja ' + str(c + 1):<12}")


# ---------------------------------------------------------------------------
# 9. Programa principal
# ---------------------------------------------------------------------------
def main():
    grafo = grafo_prueba()

    print(f"Grafo de cursos. Vértices: {', '.join(grafo.vertices())}")
    print(f"Total de conflictos (aristas): {len(obtener_aristas(grafo))}\n")

    orden_wp = orden_grado_descendente(grafo)
    colores = colorear_grafo_voraz(grafo, orden=orden_wp)

    valido, conflictos = verificar_coloreo(grafo, colores)

    print(f"Estrategia usada: orden Welsh-Powell (mayor a menor grado)")
    print(f"Colores (franjas horarias) usados: {num_colores(colores)}")
    print(f"Coloreo válido (sin choques): {'Sí' if valido else 'No'}")
    if not valido:
        print(f"Conflictos detectados: {conflictos}")
    print()

    imprimir_tabla(grafo, colores)


if __name__ == "__main__":
    main()