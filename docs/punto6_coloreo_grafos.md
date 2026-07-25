# Punto 6 — Coloreo de grafos: organizar exámenes sin choques

## 1. ¿Qué problema resuelve el programa?

El programa asigna franjas horarias de examen a un conjunto de cursos, de
forma que **dos cursos con estudiantes en común nunca queden en la misma
franja**. Esto se modela como un grafo de conflictos: cada vértice es un
curso, y una arista entre dos cursos indica que comparten al menos un
estudiante inscrito. Cada color que el programa asigna a un vértice
representa una franja horaria distinta.

El programa recibe (o construye) ese grafo de conflictos y:

- asigna un color a cada curso usando un **algoritmo voraz**;
- verifica que ningún par de cursos adyacentes haya quedado con el mismo
  color;
- reporta cuántos colores (franjas) se usaron en total y qué cursos
  quedaron en cada uno.

Se reutiliza la misma clase `Grafo` del Punto 4 (Dijkstra), en vez de
duplicar código: el coloreo no necesita pesos, así que cada conflicto se
agrega con un peso de relleno que se ignora por completo en el resto del
programa.

El grafo de conflictos puede construirse de dos formas, igual que en el
Punto 4: definido directamente en código (`grafo_prueba()`) o cargado
desde un archivo de texto (`cargar_grafo_desde_archivo()`), con una línea
por conflicto.

## 2. ¿Qué idea matemática usa?

Se implementa un **algoritmo voraz (greedy) de coloreo de grafos**.

**Idea central del algoritmo:**

1. Se recorren los vértices en un orden determinado.
2. Para cada vértice, se observan los colores que ya tienen asignados sus
   vecinos (solo los que ya fueron visitados en el recorrido).
3. Se le asigna al vértice el color más pequeño (`0, 1, 2, ...`) que
   **no** esté entre esos colores vecinos ya usados. Si todos los colores
   usados hasta el momento están ocupados por vecinos, se abre un color
   nuevo.

### ¿Por qué el algoritmo nunca deja dos vértices adyacentes con el mismo color?

Porque la regla de asignación lo impide por construcción: antes de fijar
el color de un vértice, el algoritmo revisa explícitamente los colores de
todos sus vecinos ya coloreados y descarta esos valores. Un vecino que
todavía no ha sido coloreado no puede entrar en conflicto en ese momento,
porque cuando le llegue su turno, él hará la misma verificación en sentido
contrario. Así, sin importar el orden usado, al final de la ejecución
ningún par de vértices adyacentes puede compartir color.

### ¿Por qué el orden de recorrido de los vértices puede cambiar el resultado?

Un vértice solo "ve" los colores de los vecinos que ya fueron coloreados
antes que él. Si el orden hace que un vértice muy conectado se coloree de
último, puede encontrarse con que sus vecinos ya usaron varios colores
distintos, obligándolo a abrir uno nuevo — mientras que si ese mismo
vértice se hubiera coloreado primero, habría tenido vía libre para el
color `0`. Por eso el programa usa la heurística de **Welsh-Powell**:
ordenar los vértices de mayor a menor grado antes de colorear, para que
los cursos con más conflictos se resuelvan primero, cuando hay más colores
libres disponibles.

## 3. ¿Por qué el algoritmo voraz no siempre garantiza el menor número posible de colores, pero sí produce una asignación válida?

**La validez está garantizada por construcción** (ver sección anterior):
en cada paso el algoritmo revisa los colores de los vecinos ya coloreados
y nunca reutiliza uno de ellos. Esto es una propiedad estructural del
algoritmo, no depende del orden ni de la forma del grafo — siempre se
cumple.

**La optimalidad no está garantizada**, porque el algoritmo es *voraz*:
toma en cada paso la decisión que parece mejor en ese momento (el color
más pequeño disponible) sin la posibilidad de volver atrás y reconsiderar
una elección anterior a la luz de vértices que aún no ha visto. Dos
razones concretas de por qué esto puede alejarlo del óptimo:

- **El orden importa.** En las pruebas del proyecto se usa un grafo
  bipartito de 6 vértices (`A1, A2, A3` contra `B1, B2, B3`) cuyo número
  cromático real es 2. Coloreado en el orden `A1, B1, A2, B2, A3, B3`, el
  algoritmo termina usando **3** colores; coloreado en el orden agrupado
  `A1, A2, A3, B1, B2, B3`, logra el óptimo de **2**. Mismo grafo, mismo
  algoritmo, distinto resultado — solo por el orden de recorrido.
- **La cota teórica es Δ+1, no el óptimo real.** El algoritmo voraz nunca
  usa más de `Δ + 1` colores, donde `Δ` es el grado máximo del grafo, pero
  el número cromático real (el mínimo verdadero) puede ser bastante menor
  que esa cota. Calcular ese mínimo exacto es, en el caso general, un
  problema **NP-difícil**: no se conoce ningún algoritmo eficiente que lo
  resuelva para grafos arbitrarios grandes. Por eso se usa una heurística
  rápida (voraz, con orden Welsh-Powell) en vez de buscar la solución
  óptima exacta.

En el caso de prueba del proyecto (12 cursos, 18 conflictos), el resultado
real fue:

| Franja | Cursos |
|---|---|
| 1 | Algebra, BasesDeDatos, Fisica2, SistemasOperativos |
| 2 | Estadistica, FEM, ProgramacionI, Quimica, RedesComputadores |
| 3 | Calculo, Discreta, IngSoftware |

Aquí se usaron 3 franjas, y ese mínimo de 3 sí es necesario (no es un
desperdicio del algoritmo): dentro del grafo existe un **triángulo**
—`BasesDeDatos`, `ProgramacionI` e `IngSoftware` están conectados entre
sí los tres— y tres vértices mutuamente adyacentes nunca pueden
colorearse con menos de 3 colores, sin importar qué algoritmo se use.

## 4. ¿Cómo se ejecuta?

Requisitos: Python 3.8+. No se usan librerías externas (solo `sys` y
`os`, de la biblioteca estándar). Depende del módulo `dijkstra.py` del
Punto 4 (mismo repositorio), del cual se reutiliza la clase `Grafo`.

**Ejecutar el programa interactivo:**

```bash
cd src/Grafos/punto6_coloreo_grafos
python coloreo_grafos.py
```

Esto corre el caso de prueba (12 cursos, 18 conflictos), colorea con la
heurística Welsh-Powell y muestra la tabla de resultados: curso, grado,
color y franja asignada.

**Usar las funciones puras desde otro script:**

```python
from coloreo_grafos import (
    grafo_prueba, cargar_grafo_desde_archivo, orden_grado_descendente,
    colorear_grafo_voraz, verificar_coloreo, num_colores,
)

# Opción A: grafo definido en código
g = grafo_prueba()

# Opción B: grafo cargado desde archivo de texto
g = cargar_grafo_desde_archivo("grafo_cursos.txt")

orden = orden_grado_descendente(g)
colores = colorear_grafo_voraz(g, orden=orden)

valido, conflictos = verificar_coloreo(g, colores)
print(num_colores(colores), valido)   # -> 3 True
```

**Formato del archivo de grafo** (`grafo_cursos.txt`), un conflicto por
línea:

```
# Formato: cursoA cursoB
BasesDeDatos FEM
BasesDeDatos ProgramacionI
...
```

A diferencia del cargador del Punto 4 (que exige 3 columnas porque
Dijkstra necesita un peso), aquí solo se piden 2 columnas: el coloreo no
usa distancias, solo necesita saber que el conflicto existe.

**Ejecutar las pruebas:**

```bash
python -m tests.test_6_coloreo_grafos
# o
pytest tests/test_6_coloreo_grafos.py -v
```

## 5. ¿Qué pruebas hicieron?

El archivo `tests/test_6_coloreo_grafos.py` contiene 10 casos:

| # | Caso | Qué verifica |
|---|------|---------------|
| 1 | Triángulo exige 3 colores | 3 vértices mutuamente conectados nunca se pueden colorear con menos de 3 colores |
| 2 | Orden alternado desperdicia colores | un grafo bipartito (óptimo=2) coloreado con un orden malo termina usando 3 |
| 3 | Orden agrupado alcanza el óptimo | el mismo grafo bipartito, con un orden agrupado, sí logra los 2 colores óptimos |
| 4 | Verificación detecta conflicto | un coloreo inválido armado a mano (dos vecinos con el mismo color) es detectado correctamente |
| 5 | Grado cuenta vecinos | `grado()` devuelve el número correcto de vecinos de un vértice |
| 6 | Aristas sin duplicados | `obtener_aristas()` no cuenta dos veces la misma conexión no dirigida |
| 7 | Mínimo de vértices | el grafo de prueba tiene al menos 10 vértices, como exige el enunciado |
| 8 | Coloreo válido con 3 colores | el grafo de prueba completo (12 cursos) produce un coloreo válido usando exactamente 3 colores |
| 9 | Carga desde archivo | el grafo cargado desde `.txt` tiene los mismos vértices y aristas que `grafo_prueba()`, y da el mismo resultado de coloreo |
| 10 | Formato de archivo inválido | una línea con una sola palabra (sin el segundo curso) lanza `ValueError` |

Todos los casos pasan correctamente al día de esta entrega.

## 6. ¿Qué limitaciones tiene la solución?

- El algoritmo voraz **no garantiza el número mínimo de colores** (el
  número cromático real); solo garantiza una cota superior de `Δ + 1` y
  una asignación siempre válida.
- El orden de recorrido cambia el resultado: Welsh-Powell reduce el
  riesgo de los peores casos frente a un orden arbitrario, pero tampoco
  garantiza llegar al óptimo — sigue siendo una heurística.
- El programa reutiliza la clase `Grafo` del Punto 4, que exige un peso
  por cada arista aunque el coloreo no lo necesite; ese peso se agrega
  como relleno (`peso=1`) y se ignora en todas las funciones nuevas.
- El cargador desde archivo (`cargar_grafo_desde_archivo()`) valida el
  número de columnas por línea, pero no verifica que los nombres de curso
  sean consistentes (por ejemplo, no detecta errores de tipeo como
  `"Basesdedatos"` vs `"BasesDeDatos"` — los trataría como cursos
  distintos).
- Calcular el número cromático exacto de un grafo arbitrario es un
  problema NP-difícil en general; esta solución es una heurística rápida,
  no un solver exacto.
