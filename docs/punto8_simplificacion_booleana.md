# Punto 8 — Simplificación booleana: hacer un circuito más barato

## 1. ¿Qué problema resuelve el programa?

El programa recibe una función booleana de 3 o 4 variables, definida por
la lista de minterminos donde vale 1, y produce una **expresión suma de
productos equivalente pero más simple**: la misma tabla de verdad, con
menos literales (y por lo tanto, menos compuertas si se construyera el
circuito).

Simplificar no es solo un ejercicio algebraico: cada literal de más en la
expresión final se traduce en una entrada de compuerta real, así que
reducir la expresión reduce directamente el costo del circuito.

## 2. ¿Qué idea matemática usa?

### Minterminos y tabla de verdad

Un **mintermino** es un producto (AND) de todas las variables, cada una
en su forma normal o negada, que vale 1 para exactamente **una**
combinación de entrada. El número decimal del mintermino, escrito en
binario, es justamente esa combinación: con variables A, B, C, el
mintermino 5 es `101`, es decir A·B'·C.

Dos expresiones booleanas son equivalentes si y solo si tienen **la misma
tabla de verdad** — producen 1 para exactamente los mismos minterminos —
sin importar qué tan distintas se vean algebraicamente. Por eso el
programa no confía en el álgebra a ciegas: al final recorre las 2ⁿ
combinaciones posibles y compara la función original contra la
simplificada, fila por fila.

### El algoritmo: Quine-McCluskey

La idea central es que **dos términos que difieren en un solo bit se
pueden fusionar**, porque esa variable ya no afecta el resultado. Por
ejemplo, `A·B'·C` (101) y `A·B·C` (111) difieren solo en B, así que se
combinan en `A·C` (1-1): sin importar el valor de B, la expresión vale 1.

Con el caso de prueba del taller, minterminos `{1,3,5,7}` en binario son
`001, 011, 101, 111`. Agrupándolos por cantidad de unos y combinando los
que difieren en un bit:

```
001 y 011 difieren en el bit del medio  -> 0-1
001 y 101 difieren en el primer bit     -> -01
011 y 111 difieren en el primer bit     -> -11
101 y 111 difieren en el bit del medio  -> 1-1
```

Estos cuatro términos con un guion se pueden combinar de nuevo entre
ellos (`0-1` con `1-1`, y `-01` con `-11`), y ambas combinaciones dan el
mismo resultado: `--1`. Ya no se puede simplificar más: es un
**implicante primo**. Como C es la única posición sin guion (con valor
1), la expresión final es simplemente `C` — coincide con que los cuatro
minterminos tienen a C en 1 y A, B variando libremente.

Cuando una función tiene más de un implicante primo, el programa arma
una tabla de cobertura: identifica los **implicantes esenciales**
(aquellos que son la única opción que cubre algún mintermino) y, si algo
queda sin cubrir, completa con un criterio goloso eligiendo en cada paso
el implicante que cubra más minterminos faltantes.

## 3. ¿Cómo se ejecuta?

Requisitos: Python 3.8+. No se usan librerías externas.

**Ejecutar el programa interactivo:**

```bash
cd src/Bool
python punto8_simplificacion_booleana.py
```

Ejemplo de ejecución (caso de prueba del taller):

```
Ingrese el número de variables (3 o 4): 3
Ingrese los minterminos (enteros de 0 a 7, separados por espacios):
Minterminos: 1 3 5 7

Minterminos: [1, 3, 5, 7]
Variables: ['A', 'B', 'C']

Implicantes primos encontrados:
  --1  ->  C       (cubre minterminos [1, 3, 5, 7])

Expresión simplificada: C
¿Misma tabla de verdad que la original? True
```

**Usar las funciones puras desde otro script:**

```python
from punto8_simplificacion_booleana import simplificar

resultado = simplificar([1, 3, 5, 7], num_variables=3, nombres_variables=['A', 'B', 'C'])
# resultado['expresion']   -> 'C'
# resultado['equivalente'] -> True
```

**Ejecutar las pruebas:**

```bash
python -m tests.test_8_simplificacion_booleana
# o
pytest tests/test_8_simplificacion_booleana.py -v
```

## 4. ¿Qué pruebas hicieron?

El archivo `tests/test_8_simplificacion_booleana.py` contiene 11 casos, que cubren tanto
las piezas internas del algoritmo como el resultado final:

| # | Caso | Qué verifica |
|---|------|---------------|
| 1 | Caso obligatorio del taller | minterminos `{1,3,5,7}` simplifican a `C`, con tabla de verdad equivalente |
| 2 | Conversión a binario | decimales se convierten a cadenas de bits de longitud fija correctamente |
| 3 | Combinar términos (1 bit de diferencia) | dos términos que difieren en un bit se fusionan bien |
| 4 | Combinar términos (más de 1 bit) | términos que difieren en más de un bit no se combinan |
| 5 | Combinar respeta guiones alineados | términos con guiones en posiciones distintas no se combinan |
| 6 | Implicantes primos, caso mínimo | un solo mintermino no tiene con qué combinarse y queda como implicante completo |
| 7 | Selección de esenciales | el único implicante primo de un caso simple queda seleccionado |
| 8 | Traducción a expresión | los bits se traducen bien a literales (normal, negado, omitido, o constante `1`) |
| 9 | Verificación detecta error | una expresión que no corresponde a la función es marcada como no equivalente |
| 10 | Cobertura no trivial (4 variables) | un caso con varios implicantes primos se cubre correctamente combinando esenciales y cobertura golosa |
| 11 | Función que cubre todo el espacio | cuando la función vale 1 en todas las combinaciones, la expresión colapsa a la constante `1` |

Todos los casos pasan correctamente al día de esta entrega.

## 5. ¿Qué limitaciones tiene la solución?

- El menú de consola solo admite funciones de 3 o 4 variables, tal como
  pide el enunciado; el algoritmo en sí no tiene esa restricción, es una
  limitación de la interfaz.
- El paso de cobertura, tras tomar los implicantes esenciales, usa un
  criterio goloso (mayor número de minterminos faltantes cubiertos). Para
  funciones de 3-4 variables esto encuentra en la práctica la cobertura
  óptima, pero a diferencia de una búsqueda exhaustiva no está
  matemáticamente garantizado que sea siempre el mínimo global de
  literales en todos los casos posibles.
- No se implementan condiciones de indiferencia (*don't cares*); el
  enunciado no las pide, pero es una extensión típica de Quine-McCluskey
  que queda fuera del alcance de este ejercicio.
- La verificación por tabla de verdad recorre 2ⁿ combinaciones, lo cual es
  trivial para 3-4 variables pero no escalaría bien a funciones con
  muchas más variables.