# Punto 4 — Ruta más corta: una ciudad como grafo

## 1. ¿Qué problema resuelve el programa?

El programa modela una red de transporte urbano como un grafo ponderado: cada
vértice es un punto de la ciudad (una estación, un portal, un punto de interés)
y cada arista es una conexión directa entre dos puntos, con un peso que
representa el tiempo o la distancia de viaje entre ellos.

El objetivo es, dados dos puntos de la ciudad (origen y destino), encontrar
**la ruta de menor costo total** para ir de uno a otro, y reportar tanto la
distancia acumulada como la secuencia exacta de puntos que conforman esa ruta.

## 2. ¿Qué idea matemática usa?

Se implementa el **algoritmo de Dijkstra**, un algoritmo voraz (*greedy*) para
encontrar caminos mínimos en grafos ponderados con pesos no negativos.

**Idea central del algoritmo:**

1. Se inicializa la distancia al vértice origen en `0` y la de todos los demás
   vértices en `infinito`.
2. Se usa una cola de prioridad (min-heap) que siempre entrega el vértice no
   visitado con menor distancia acumulada conocida.
3. Al "visitar" un vértice, se revisan todos sus vecinos: si llegar a un
   vecino pasando por el vértice actual es más corto que la mejor distancia
   conocida hasta ahora, se actualiza esa distancia (paso de **relajación de
   aristas**) y se guarda de dónde vino (para poder reconstruir la ruta al
   final).
4. El proceso termina cuando se visita el vértice destino, o cuando la cola
   se vacía (no hay más vértices alcanzables).
5. La ruta se reconstruye recorriendo hacia atrás el arreglo de "predecesores"
   desde el destino hasta el origen.

### ¿Por qué Dijkstra necesita pesos no negativos?

El algoritmo asume que, una vez que un vértice se marca como visitado con su
distancia mínima, **ningún camino futuro podrá mejorar esa distancia**. Esto
solo es válido si sumar una arista nunca puede disminuir el total acumulado,
es decir, si todos los pesos son `≥ 0`.

Si existiera una arista con peso negativo, podría aparecer más adelante un
camino con más aristas pero con una suma total menor, lo cual invalidaría una
distancia que el algoritmo ya había dado por "cerrada" (definitiva). En ese
caso el resultado de Dijkstra sería incorrecto. Para grafos con pesos
negativos existen otros algoritmos, como Bellman-Ford, que sí toleran esa
situación (siempre que no haya ciclos de peso negativo).

### ¿Qué significa que un camino sea óptimo?

Un camino óptimo entre dos vértices `u` y `v` es aquel cuya **suma de pesos de
las aristas que lo componen es la mínima posible** entre todos los caminos
posibles que conectan `u` con `v` en el grafo.

Dijkstra garantiza que el camino que reconstruye es óptimo porque en cada paso
expande primero el vértice no visitado con menor distancia acumulada conocida.
Gracias a que los pesos son no negativos, en el momento en que un vértice se
marca como visitado ya no existe ningún otro camino que pueda ofrecerle una
distancia menor, así que su valor queda fijado como definitivo y correcto.

## 3. ¿Cómo se ejecuta?

Requisitos: Python 3.8 o superior. No se usan librerías externas (solo
`heapq` y `math`, que son parte de la biblioteca estándar).

**Ejecutar la demostración por consola:**

```bash
cd src/grafos
python dijkstra.py
```

Esto corre el grafo de prueba (definido en código) y muestra la ruta más
corta para tres parejas de vértices distintas.

**Usar el módulo desde otro script:**

```python
from dijkstra import grafo_prueba, cargar_grafo_desde_archivo, dijkstra

# Opción A: grafo definido en código
g = grafo_prueba()

# Opción B: grafo cargado desde archivo de texto
g = cargar_grafo_desde_archivo("grafo_ciudad.txt")

distancia, ruta = dijkstra(g, "Portal", "Estadio")
print(distancia, ruta)
```

**Formato del archivo de grafo** (`grafo_ciudad.txt`), una arista por línea:

```
origen destino peso
Portal Calle26 5
Calle26 Museo 3
...
```

**Ejecutar las pruebas:**

```bash
# Desde la raíz del repositorio
python -m tests.test_dijkstra
```

o, si se tiene `pytest` instalado:

```bash
pytest tests/test_dijkstra.py -v
```

## 4. ¿Qué pruebas hicieron?

El archivo `tests/test_dijkstra.py` contiene 7 casos:

| # | Caso | Entrada | Salida esperada |
|---|------|---------|------------------|
| 1 | Ruta normal | origen=`Portal`, destino=`Estadio` | distancia=16, ruta=`Portal→Calle26→Museo→Centro→Estadio` |
| 2 | Otra ruta normal | origen=`Universidad`, destino=`Terminal` | distancia=9, ruta=`Universidad→Centro→Terminal` |
| 3 | Origen = destino | origen=destino=`Museo` | distancia=0, ruta=`[Museo]` |
| 4 | Vértice desconectado | destino=`Aeropuerto` (sin aristas) | distancia=infinito, ruta=`[]` |
| 5 | Vértice inexistente | destino=`NoExiste` | lanza `ValueError` |
| 6 | Peso negativo | arista con peso `-3` | lanza `ValueError` al construir el grafo |
| 7 | Carga desde archivo | mismo grafo cargado desde `.txt` | debe dar el mismo resultado que el grafo definido en código |

Todos los casos pasan correctamente al día de esta entrega.

## 5. ¿Qué limitaciones tiene la solución?

- El grafo de prueba es no dirigido (las conexiones funcionan en ambos
  sentidos). El código sí soporta grafos dirigidos mediante el parámetro
  `dirigido=True` en `agregar_arista`, pero el grafo de ejemplo no lo usa.
- No se maneja el caso de pesos negativos: el programa los rechaza
  explícitamente (lanzando `ValueError`), en vez de intentar ejecutarlos con
  un resultado potencialmente incorrecto.
- La complejidad del algoritmo con la implementación usada (cola de prioridad
  binaria vía `heapq`) es `O((V + E) log V)`, adecuada para grafos pequeños o
  medianos como el de este taller, pero no optimizada para redes de
  transporte reales con millones de nodos.
- El programa encuentra **una** ruta óptima; si existen varias rutas con la
  misma distancia mínima, solo se devuelve una de ellas (la primera que el
  algoritmo encuentra según el orden de exploración).