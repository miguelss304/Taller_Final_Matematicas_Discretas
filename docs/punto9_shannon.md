# Punto 9 — Shannon: medir información en un mensaje

## 1. ¿Qué problema resuelve el programa?

El programa mide cuánta **información** (o incertidumbre) contiene un
texto, usando la entropía de Shannon. Para uno o varios textos, calcula:

- la frecuencia de cada símbolo (carácter);
- la probabilidad de cada símbolo dentro del texto;
- la entropía total del texto;
- y, si se ingresan varios textos, indica cuál de ellos tiene mayor
  entropía (es decir, cuál es más "impredecible" o variado).

## 2. ¿Qué idea matemática usa?

Se usa la fórmula de la **entropía de Shannon**:

```
H = - Σ p_i · log2(p_i)
```

donde `p_i` es la probabilidad de que aparezca el símbolo `i` en el texto
(su frecuencia dividida entre la longitud total del texto).

El programa calcula esto en tres pasos:

1. **Conteo** (`contar_letras`): cuenta cuántas veces aparece cada
   carácter en el texto.
2. **Probabilidad** (`calcular_probabilidad`): divide cada conteo entre
   la longitud total del texto, obteniendo `p_i` para cada símbolo.
3. **Entropía** (`calcular_entropia`): aplica la fórmula de Shannon sobre
   esas probabilidades.

### ¿Por qué la entropía mide incertidumbre y no simplemente longitud del texto?

La entropía no depende de cuántos caracteres tiene el texto, sino de
**qué tan distribuidas están las probabilidades de sus símbolos**.

- Un texto de 1000 letras, todas iguales (por ejemplo `"AAAA...A"`), tiene
  entropía **0**: no importa qué tan largo sea, siempre se sabe con
  certeza absoluta cuál será el siguiente carácter (`A`). No hay ninguna
  sorpresa al leerlo.
- Un texto de solo 4 letras distintas y equiprobables (por ejemplo
  `"ABCD"`) tiene una entropía de `log2(4) = 2` bits: cada símbolo es
  igual de probable que cualquier otro, así que hay máxima incertidumbre
  sobre cuál vendrá a continuación.

Es decir, la entropía mide cuánta "sorpresa" promedio hay al leer cada
símbolo del mensaje, no cuántos símbolos tiene el mensaje. Dos textos
pueden tener longitudes muy distintas y aun así tener entropías similares
(o al revés: la misma longitud, y entropías muy distintas), dependiendo de
qué tan repetitivos o variados sean sus símbolos.

## 3. ¿Cómo se ejecuta?

Requisitos: Python 3.8+. No se usan librerías externas (solo `math`, de la
biblioteca estándar).

**Ejecutar el programa interactivo:**

```bash
cd "src/Cuantica/Punto 9 Taller MD"
python3 shannon.py
```

Ejemplo de ejecución:

```
Ingrese la cantidad de textos que desea comparar: 2
Ingrese el texto 1: AAAAA
Ingrese el texto 2: HOLA MUNDO
```

Salida (resumida):

```
Texto: AAAAA
Entropía: -0.000

Texto: HOLA MUNDO
Entropía: 3.122

El texto con mayor entropía es: 'HOLA MUNDO' con una entropía de 3.122
```

**Usar las funciones puras desde otro script:**

```python
from shannon import analizar_texto

cantidad_letras, probabilidades, entropia = analizar_texto("HOLA MUNDO")
print(entropia)  # 3.122...
```

**Ejecutar las pruebas:**

```bash
python -m tests.test_9_shannon
# o
pytest tests/test_9_shannon.py -v
```

## 4. ¿Qué pruebas hicieron?

El archivo `tests/test_9_shannon.py` contiene 6 casos:

| # | Caso | Entrada | Salida esperada |
|---|------|---------|------------------|
| 1 | Conteo básico | `"AAB"` | `{'A': 2, 'B': 1}` |
| 2 | Probabilidad calculada | conteo `{'A':2,'B':2}` sobre `"AABB"` | `{'A': 0.5, 'B': 0.5}` |
| 3 | Texto totalmente repetitivo | `"AAAAA"` | entropía ≈ 0 |
| 4 | Dos símbolos equiprobables | `"ABAB"` | entropía = 1.0 (un bit exacto) |
| 5 | Variado vs. repetitivo | `"HOLA MUNDO"` vs `"AAAAAAAAAA"` | el variado tiene mayor entropía |
| 6 | Cuatro símbolos equiprobables (directo) | `{'A':.25,'B':.25,'C':.25,'D':.25}` | entropía = 2.0 (`log2(4)`) |

Todos los casos pasan correctamente al día de esta entrega.

## 5. ¿Qué limitaciones tiene la solución?

- El programa trata cada **carácter individual** como símbolo, incluyendo
  espacios y signos de puntuación. No agrupa por palabras ni distingue
  mayúsculas de minúsculas como símbolos separados si el usuario mezcla
  ambas.
- Solo mide la entropía de orden cero (basada únicamente en la frecuencia
  individual de cada símbolo). No considera la dependencia entre
  caracteres consecutivos (por ejemplo, que en español la letra `Q` casi
  siempre va seguida de `U`), que daría una medida de entropía condicional
  más ajustada al idioma real.
- La extensión opcional de Huffman (comparar la entropía con la longitud
  promedio de un código de compresión real) no está implementada en esta
  versión.
- Con textos muy cortos (una o dos letras), la entropía calculada puede no
  ser representativa del comportamiento estadístico real de un idioma.