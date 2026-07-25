# Punto 3 — MPC básico: calcular un promedio sin mostrar los datos

## 1. ¿Qué problema resuelve el programa?

El programa simula un protocolo simplificado de **Computación Multipartita
Segura (MPC)**: varias personas (aquí, tres servidores) quieren calcular
conjuntamente la suma y el promedio de un conjunto de notas, **sin que
ninguno de los servidores llegue a ver la lista completa de notas
originales**.

Cada estudiante tiene una nota entre 0 y 50. El programa reparte cada nota
en tres partes aleatorias, entrega una parte a cada servidor, y solo al
final combina las tres sumas parciales para obtener el resultado real
(suma total y promedio).

## 2. ¿Qué idea matemática usa?

Se usa **aritmética modular**, concretamente la técnica de "compartir un
secreto" mediante una suma módulo `M` (una versión simplificada de lo que
en criptografía se llama *secret sharing aditivo*).

### ¿Cómo se escribe una nota x como x ≡ s1 + s2 + s3 (mód M)?

Supongamos una nota `x = 42` y un módulo `M = 1000003`.

1. Se eligen dos números aleatorios `s1` y `s2` entre `0` y `M-1`. Por
   ejemplo: `s1 = 733021`, `s2 = 291584` (números elegidos al azar, sin
   relación aparente con `42`).
2. Se calcula la tercera parte para que la suma cuadre exactamente módulo
   `M`:
   ```
   s3 = (x - s1 - s2) mod M
      = (42 - 733021 - 291584) mod M
      = 975420   (por ejemplo)
   ```
3. Ahora se cumple que `(s1 + s2 + s3) mod M = 42`, es decir, se recupera
   la nota original — pero solo si se conocen **las tres partes juntas**.

**¿Por qué una sola parte no revela nada sobre x?**
Porque `s1` y `s2` se generaron completamente al azar entre `0` y `M-1`,
sin ninguna relación con `x`. Si un servidor solo tiene `s1 = 733021`, ese
número podría corresponder a *cualquier* nota posible entre 0 y 50 (para
cada nota existe alguna combinación de `s2, s3` que la reconstruye junto
con ese `s1`). Es decir, `s1` por sí solo no reduce en nada la
incertidumbre sobre cuál era la nota real. Solo cuando se combinan las
tres partes con la operación módulo `M` aparece la nota original.

## 3. ¿Cómo se ejecuta?

Requisitos: Python 3.8+. No se usan librerías externas (solo `random`, de
la biblioteca estándar).

**Ejecutar el programa interactivo:**

```bash
cd "src/Criptografia/Punto 3 Taller MD"
python mpc.py
```

Ejemplo de ejecución:

```
Ingrese el total de notas a ingresar: 4
Ingrese las notas (de 0 a 50):
Nota 1: 40
Nota 2: 35
Nota 3: 50
Nota 4: 25
Suma total de las notas: 150
Promedio de las notas: 37.5
```

**Usar las funciones puras desde otro script:**

```python
from mpc import repartir_notas, suma_servidor, reconstruir_suma_y_promedio

M = 1000003
notas = [40, 35, 50, 25]

s1, s2, s3 = repartir_notas(notas, M)
S1 = suma_servidor(s1, M)
S2 = suma_servidor(s2, M)
S3 = suma_servidor(s3, M)

suma_total, promedio = reconstruir_suma_y_promedio(S1, S2, S3, M, len(notas))
# suma_total=150, promedio=37.5
```

**Ejecutar las pruebas:**

```bash
python -m tests.test_3_mpc
# o
pytest tests/test_3_mpc.py -v
```

## 4. ¿Qué pruebas hicieron?

El archivo `tests/test_3_mpc.py` contiene 6 casos. Como el reparto de notas
usa números aleatorios, las pruebas no verifican valores fijos de `s1`,
`s2`, `s3`, sino las **propiedades matemáticas** que el protocolo debe
cumplir siempre, sin importar qué salga al azar:

| # | Caso | Qué verifica |
|---|------|---------------|
| 1 | Ejemplo del taller | notas=`[40,35,50,25]` reconstruye suma=150, promedio=37.5 |
| 2 | Una sola nota | dividir y volver a sumar una nota devuelve la nota original |
| 3 | Suma coincide con la real (20 repeticiones) | la reconstrucción es correcta sin importar el reparto aleatorio |
| 4 | Promedio no entero | `[10, 15]` da promedio=12.5, no se redondea a 12 |
| 5 | Ninguna parte revela la nota | ninguna de las 3 partes individuales es igual a la nota original (20 repeticiones) |
| 6 | Distintos tamaños de lista | funciona con listas de 1, 3 y 5 notas |

Todos los casos pasan correctamente al día de esta entrega.

## 5. ¿Qué limitaciones tiene la solución?

- Es una **simulación educativa**, no un protocolo MPC de nivel productivo.
  No incluye comunicación real entre servidores independientes (todo corre
  en el mismo programa) ni mecanismos de verificación de que los
  servidores actúen honestamente.
- La seguridad de "una parte no revela nada" depende de que `M` sea lo
  suficientemente grande frente al rango de las notas (0–50). Con
  `M = 1 000 003` esto se cumple ampliamente, pero si `M` fuera muy pequeño
  (por ejemplo `M = 51`), sí podría filtrarse información.
- El protocolo solo soporta la operación de **suma** (y, por extensión, el
  promedio). No permite calcular otras funciones (máximo, mediana,
  varianza) sin technicas MPC adicionales.
- Si dos de los tres servidores se coluden (comparten sus partes entre
  sí), sí pueden reconstruir la nota original de un estudiante, ya que
  basta con conocer `s1 + s2` y despejar `s3` (o de forma directa, ya que
  con 2 de 3 partes y la fórmula se puede inferir la tercera). Este
  esquema simplificado no es resistente a colusión.