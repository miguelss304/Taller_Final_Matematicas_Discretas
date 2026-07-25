# Punto 10 — Primer simulador cuántico: bits, qubits y mediciones

## 1. ¿Qué problema resuelve el programa?

El programa simula, de forma matemática y sin usar hardware cuántico
real, el comportamiento de un solo **qubit**. Permite:

- Representar el estado de un qubit como un vector de dos entradas
  (números complejos).
- Aplicar las compuertas cuánticas `X`, `Z` y `H` sobre ese estado.
- Calcular las probabilidades de medir `0` o `1` a partir del estado.
- Simular 1000 mediciones independientes y reportar las frecuencias
  observadas, ilustrando el carácter probabilístico de la medición
  cuántica.

## 2. ¿Qué idea matemática usa?

Un qubit se representa como una **combinación lineal** (superposición) de
los dos estados base clásicos:

```
|psi> = alpha |0> + beta |1>,   representado como el vector [alpha, beta]
```

donde `alpha` y `beta` son números complejos que cumplen
`|alpha|^2 + |beta|^2 = 1`. Los valores `|alpha|^2` y `|beta|^2` son,
respectivamente, las probabilidades de que una medición del qubit
resulte en `0` o en `1`.

**Aplicar una compuerta** cuántica es simplemente multiplicar la matriz
de la compuerta (2×2) por el vector de estado (una multiplicación
matriz-vector estándar):

```
X = [[0, 1],       Z = [[1,  0],      H = 1/√2 · [[1,  1],
     [1, 0]]            [0, -1]]                   [1, -1]]
```

- **X** ("bit flip"): intercambia las amplitudes de `|0>` y `|1>`, el
  equivalente cuántico de la compuerta NOT clásica.
- **Z** ("phase flip"): deja `|0>` intacto, pero invierte el signo de la
  amplitud de `|1>` (cambia su fase, sin alterar las probabilidades).
- **H** (Hadamard): crea una superposición equilibrada. Aplicada sobre
  `|0>`, produce un estado con **50% de probabilidad** de medir `0` y
  50% de medir `1`.

**Medir** el qubit es un proceso probabilístico: se genera un número
aleatorio y, según caiga por debajo o por encima de la probabilidad de
`0`, el resultado "colapsa" a `0` o a `1`. Repetir esta medición 1000
veces sobre el mismo estado permite observar experimentalmente que las
frecuencias relativas se acercan a las probabilidades teóricas
(`|alpha|^2`, `|beta|^2`).

## 3. ¿Cómo se ejecuta?

Requisitos: Python 3.8+. No se usan librerías externas (solo `cmath` y
`random`, de la biblioteca estándar; no se requiere numpy).

**Ejecutar el programa interactivo:**

```bash
python src/Cuantica/punto10_qubit.py
```

Salida esperada (resumida):

```
Caso 1: X|0>
X|0>: [0j, (1+0j)]
  P(0) = 0.000, P(1) = 1.000
  ¿Es igual a |1>? True

Caso 2: H|0>
H|0>: [(0.707...+0j), (0.707...+0j)]
  P(0) = 0.500, P(1) = 0.500
  Mediciones simuladas (1000): 0 -> ~500 veces, 1 -> ~500 veces

Caso 3: H(H|0>)
HH|0>: [(0.999...+0j), 0j]
  ¿Es igual a |0>? True
```

**Usar las funciones puras desde otro script:**

```python
from punto10_qubit import ESTADO_0, COMPUERTA_H, aplicar_compuerta, calcular_probabilidades

estado_h = aplicar_compuerta(COMPUERTA_H, ESTADO_0)
prob_0, prob_1 = calcular_probabilidades(estado_h)  # -> (0.5, 0.5)
```

**Ejecutar las pruebas:**

```bash
python -m tests.test_10_qubit
# o
pytest tests/test_10_qubit.py -v
```

## 4. ¿Qué pruebas hicieron?

El archivo `tests/test_10_qubit.py` contiene 8 casos, incluyendo los 3
obligatorios del enunciado:

| # | Caso | Qué verifica |
|---|------|---------------|
| 1 (obligatorio) | `X|0> = |1>` | aplicar X a `|0>` da exactamente `|1>` |
| 2 (obligatorio) | `H|0>` da 50%/50% | las probabilidades calculadas son ambas 0.5 |
| 3 (obligatorio) | `HH|0> = |0>` | aplicar H dos veces regresa al estado original (con tolerancia numérica) |
| 4 | X es su propia inversa | aplicar X dos veces también regresa a `|0>` |
| 5 | Z sobre `|0>` no cambia el estado | Z solo afecta la fase de `|1>`, no de `|0>` |
| 6 | Las probabilidades suman 1 | para varios estados distintos, `P(0)+P(1)=1` |
| 7 | 1000 mediciones de `|0>` siempre dan 0 | sin superposición, no hay aleatoriedad en el resultado |
| 8 | 1000 mediciones de `H|0>` cercanas a 50/50 | el conteo de ceros cae dentro de `[400, 600]` |

Todos los casos pasan correctamente al día de esta entrega, incluso
ejecutando el archivo varias veces (para confirmar estabilidad frente a
la aleatoriedad de las mediciones simuladas).

## 5. ¿Qué diferencia hay entre la probabilidad cuántica simulada y la ejecución en un computador cuántico real?

En este simulador, la "medición" es en realidad un experimento clásico:
se calculan las probabilidades exactas a partir del estado (que se
conoce en todo momento, como números de punto flotante en la memoria del
computador), y luego se usa un generador de números pseudoaleatorios
clásico (`random.random()`) para decidir el resultado de cada medición
simulada. El estado nunca "colapsa" físicamente; solo se descarta
después de simular la lectura.

En un **computador cuántico real**, el estado del qubit no es un número
que el programador pueda leer directamente en ningún momento: existe
físicamente como una superposición genuina (por ejemplo, codificada en el
spin de una partícula o en el estado de un circuito superconductor), y
solo al medirlo se produce un colapso físico irreversible a `0` o `1`,
gobernado por las leyes de la mecánica cuántica y no por un algoritmo de
números aleatorios. Además, en hardware real el estado es susceptible a
**ruido y decoherencia** (interacción no deseada con el entorno), lo cual
introduce errores que no existen en esta simulación matemática idealizada.

En resumen: la simulación reproduce fielmente las *probabilidades*
predichas por la teoría cuántica, pero no reproduce el fenómeno físico
real de la superposición ni el colapso genuino de la función de onda, que
solo ocurren en hardware cuántico verdadero.

## 6. ¿Qué limitaciones tiene la solución?

- Solo simula **un** qubit; no modela sistemas de múltiples qubits ni
  fenómenos como el entrelazamiento (*entanglement*), que requieren
  vectores de estado de dimensión `2^n` y matrices más grandes.
- No implementa compuertas de dos qubits (como CNOT), ni mediciones
  parciales sobre un subconjunto de qubits en un sistema mayor.
- El generador de números aleatorios es el de la biblioteca estándar de
  Python (pseudoaleatorio), suficiente para esta simulación educativa,
  pero no comparable a una fuente de aleatoriedad cuántica genuina.
- No se modelan errores de hardware real (ruido, decoherencia, tiempos de
  coherencia limitados), que sí afectan a los computadores cuánticos
  físicos actuales.