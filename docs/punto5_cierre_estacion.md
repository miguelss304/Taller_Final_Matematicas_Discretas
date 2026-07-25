# Punto 5 — Cierre de una estación: medir el impacto en la red

## 1. ¿Qué problema resuelve el programa?

El programa mide cuánto afecta a una red de transporte el cierre de un
punto importante (una estación/vértice, o una conexión específica/arista).
Para varios pares origen-destino, calcula la ruta más corta **antes** y
**después** del cierre, y reporta si la distancia aumentó, se mantuvo
igual, o si el par quedó completamente desconectado.

Se reutiliza el mismo grafo de ciudad y la misma implementación de
Dijkstra del Punto 4, en vez de duplicar código.

## 2. ¿Qué idea matemática usa?

El programa se apoya directamente en el algoritmo de Dijkstra (Punto 4)
para calcular caminos mínimos, y añade una idea adicional: **comparar dos
versiones del mismo grafo** (una completa y otra con un vértice o arista
eliminado) para medir el efecto de esa eliminación sobre las distancias
más cortas.

Formalmente, sea `G` el grafo original y `G'` el grafo tras eliminar un
vértice `v` (junto con todas sus aristas incidentes) o una arista
específica `(u, w)`. Para cada par `(origen, destino)`:

```
distancia_antes  = dijkstra(G,  origen, destino)
distancia_despues = dijkstra(G', origen, destino)
diferencia = distancia_despues - distancia_antes
```

Si en `G'` ya no existe ningún camino entre `origen` y `destino`,
`distancia_despues` se considera `infinito`, y el par se reporta como
**DESCONECTADO** (en vez de intentar calcular una diferencia numérica sin
sentido).

## 3. ¿Cuál vértice o arista cerraron y por qué ese cierre produce (o no) un impacto importante?

En el caso de prueba principal se simula el **cierre del vértice
"Centro"**. Se eligió este vértice porque, en el grafo de la ciudad
definido en el Punto 4, es el que tiene más conexiones directas (con
Calle26, Museo, Universidad, Terminal y Estadio) — es decir, funciona como
un **nodo central o "hub"** de la red.

Al ejecutar el programa con cinco pares de prueba se observa:

| Origen | Destino | Antes | Después | Diferencia | Estado |
|---|---|---|---|---|---|
| Portal | Estadio | 16 | 17 | 1 | AUMENTÓ |
| Portal | Parque | 17 | 17 | 0 | SIN CAMBIO |
| Universidad | Terminal | 9 | 16 | 7 | AUMENTÓ |
| Calle26 | Estadio | 11 | 16 | 5 | AUMENTÓ |
| Museo | Parque | 9 | 9 | 0 | SIN CAMBIO |

**Interpretación:** cerrar un nodo tan conectado como "Centro" sí produce
un impacto notorio en varias rutas (algunas aumentan su distancia hasta en
7 unidades), porque muchos caminos mínimos pasaban por él como atajo. Sin
embargo, no todos los pares se ven afectados: rutas como Portal→Parque o
Museo→Parque tienen caminos alternativos igual de cortos que no dependían
de "Centro", así que su distancia queda igual.

Esto ilustra un principio general de redes: **el impacto de cerrar un
nodo depende de cuántos caminos mínimos dependían de él**, no simplemente
de cuántas conexiones directas tenía. Un nodo muy conectado pero
"redundante" (con rutas alternativas igual de buenas) puede cerrarse sin
gran impacto, mientras que un nodo puente (sin alternativas) puede incluso
desconectar por completo partes de la red, como se muestra en las pruebas
con un grafo pequeño de ejemplo (ver sección de pruebas).

## 4. ¿Cómo se ejecuta?

Requisitos: Python 3.8+. No se usan librerías externas (solo `copy`,
`math`, de la biblioteca estándar). Depende del módulo `dijkstra.py` del
Punto 4 (mismo repositorio).

**Ejecutar el programa interactivo:**

```bash
cd "src/Grafos/Punto 5 Taller MD"
python cierre_estacion.py
```

Esto corre el caso de prueba con el cierre del vértice `"Centro"` y
muestra la tabla comparativa para 5 pares origen-destino.

**Usar las funciones puras desde otro script:**

```python
from cierre_estacion import cerrar_vertice, cerrar_arista, calcular_impacto
from dijkstra import grafo_prueba

g_antes = grafo_prueba()
g_despues = cerrar_vertice(g_antes, "Centro")   # o cerrar_arista(g_antes, "Museo", "Centro")

pares = [("Portal", "Estadio"), ("Universidad", "Terminal")]
filas = calcular_impacto(g_antes, g_despues, pares)
```

**Ejecutar las pruebas:**

```bash
python -m tests.test_5_cierre_estacion
# o
pytest tests/test_5_cierre_estacion.py -v
```

## 5. ¿Qué pruebas hicieron?

El archivo `tests/test_5_cierre_estacion.py` contiene 7 casos:

| # | Caso | Qué verifica |
|---|------|---------------|
| 1 | Cerrar vértice elimina sus aristas | ningún vértice restante sigue apuntando al cerrado |
| 2 | El grafo original no se modifica | `cerrar_vertice` trabaja sobre una copia, no muta el grafo original |
| 3 | Cerrar una arista específica | solo se afecta esa conexión puntual, el resto del vértice queda intacto |
| 4 | Detecta aumento de distancia | Universidad→Terminal aumenta tras cerrar "Centro" |
| 5 | Detecta que no hay cambio | Portal→Parque queda igual tras el cierre |
| 6 | Detecta desconexión total | grafo pequeño con un "puente"; al cerrarlo, A y B quedan desconectados |
| 7 | Procesa 5+ pares a la vez | se prueban los 5 pares exigidos por el enunciado en una sola llamada |

Todos los casos pasan correctamente al día de esta entrega.

## 6. ¿Qué limitaciones tiene la solución?

- El programa solo simula el cierre de **un** vértice o **una** arista a
  la vez; no evalúa combinaciones de cierres múltiples simultáneos.
- La comparación de "impacto" se basa únicamente en el cambio de
  distancia entre pares específicos; no calcula una métrica global única
  (como el promedio de aumento sobre todos los pares posibles de la red).
- Al cerrar un vértice, se asume que ese vértice deja de estar disponible
  también como destino u origen; si el par de prueba incluye justamente
  al vértice cerrado, se reporta directamente como desconectado.
- Se reutiliza la misma limitación de Dijkstra del Punto 4: solo funciona
  con pesos no negativos.