# Punto 7 — Tablas de verdad y circuitos lógicos

## 1. ¿Qué problema resuelve el programa?

El programa genera la **tabla de verdad completa** (las 8 combinaciones
posibles de A, B, C) para tres expresiones booleanas, y además permite
evaluar cualquiera de esas expresiones para una entrada concreta que
ingrese el usuario. Las expresiones incluidas son:

1. `(A ∧ B) ∨ (¬C)`
2. `(A ⊕ B) ∧ C`
3. `(A ∨ B) ∧ (¬A ∨ C)`

## 2. ¿Qué idea matemática usa?

Cada expresión booleana es una función que toma valores de verdad
(`Verdadero`/`Falso`) para sus variables de entrada y produce un único
valor de verdad como resultado, combinando los operadores lógicos AND
(`∧`), OR (`∨`), NOT (`¬`) y XOR (`⊕`).

Una **tabla de verdad** enumera exhaustivamente todas las combinaciones
posibles de valores de entrada (`2^n` filas para `n` variables; aquí,
`2^3 = 8` filas para A, B, C) y muestra el resultado de la expresión en
cada una. Se genera con `itertools.product([False, True], repeat=3)`,
que produce sistemáticamente las 8 combinaciones sin necesidad de anidar
manualmente tres bucles `for`.

### ¿Cómo se relaciona una tabla de verdad con un circuito lógico?

Cada operador lógico de una expresión booleana corresponde exactamente a
una **compuerta lógica** en un circuito digital: `∧` es una compuerta AND,
`∨` es una compuerta OR, `¬` es un inversor (NOT), y `⊕` es una compuerta
XOR. Una expresión booleana completa, como `(A ∧ B) ∨ (¬C)`, describe
exactamente cómo conectar esas compuertas entre sí: primero la salida de
una compuerta AND (con entradas A y B) se combina mediante una compuerta
OR con la salida de un inversor (con entrada C).

La tabla de verdad de la expresión es, entonces, exactamente la misma
tabla que describiría el comportamiento eléctrico del circuito
correspondiente: para cada combinación de señales de entrada (alto/bajo,
1/0, verdadero/falso), la tabla indica qué señal de salida producirá el
circuito. Por eso, verificar una expresión booleana con su tabla de
verdad es equivalente a simular el comportamiento del circuito digital
que la implementa, sin necesidad de construirlo físicamente.

## 3. Corrección de un error encontrado en el código original

Al revisar la implementación de la expresión 3, `(A ∨ B) ∧ (¬A ∨ C)`, se
encontró un error: el segundo término se calculaba reutilizando por error
la variable del primer término (`p`, que representa `A ∨ B`), en vez de
usar `¬A` como corresponde. Esto hacía que el programa calculara en
realidad `(A ∨ B) ∧ ((A ∨ B) ∨ C)`, una expresión distinta a la pedida.

**Ejemplo donde el error se manifestaba:** con `A=True, B=True, C=False`:

- Expresión correcta: `(A∨B) ∧ (¬A∨C)` = `(T∨T) ∧ (F∨F)` = `True ∧ False` = **False**
- Cálculo con el error original: `(A∨B) ∧ ((A∨B)∨C)` = `True ∧ (True∨False)` = `True ∧ True` = **True** ❌

La corrección consistió en calcular explícitamente `termino2 = (not a) or c`
en vez de reutilizar `p`. Este caso específico quedó cubierto como prueba
(`test_expresion_3_caso_del_bug_corregido`) para evitar que el error se
reintroduzca en el futuro.

## 4. ¿Cómo se ejecuta?

Requisitos: Python 3.8+. No se usan librerías externas (solo
`itertools`, de la biblioteca estándar).

**Ejecutar el programa interactivo:**

```bash
python src/Bool/punto7_tablas_verdad.py
```

El programa imprime primero las 3 tablas de verdad completas, y al final
pide A, B, C para evaluar una entrada concreta.

**Usar las funciones puras desde otro script:**

```python
from punto7_tablas_verdad import evaluar_expresion_1, generar_tabla_verdad

resultado = evaluar_expresion_1(True, False, True)  # -> False
tabla = generar_tabla_verdad(evaluar_expresion_1)     # -> lista de 8 tuplas
```

**Ejecutar las pruebas:**

```bash
python -m tests.test_7_tablas_verdad
# o
pytest tests/test_7_tablas_verdad.py -v
```

## 5. ¿Qué pruebas hicieron?

El archivo `tests/test_7_tablas_verdad.py` contiene 6 casos:

| # | Caso | Entrada | Salida esperada |
|---|------|---------|------------------|
| 1 | Expresión 1, ¬C domina | A=F, B=F, C=F | `True` |
| 2 | Expresión 1, resultado falso | A=F, B=F, C=V | `False` |
| 3 | Expresión 2, comportamiento del XOR | A=B=V (XOR=F); A=V,B=F,C=V; A=V,B=F,C=F | `False`, `True`, `False` respectivamente |
| 4 | Expresión 3, caso específico del bug corregido | A=V, B=V, C=F | `False` (el código con el bug original daba `True`) |
| 5 | Expresión 3, resultado verdadero | A=F, B=V, C=V | `True` |
| 6 | La tabla de verdad tiene las 8 combinaciones | — | 8 filas, sin combinaciones repetidas ni faltantes |

Todos los casos pasan correctamente al día de esta entrega.

## 6. ¿Qué limitaciones tiene la solución?

- El programa solo soporta expresiones fijas, codificadas directamente
  como funciones de Python (`evaluar_expresion_1`, `2`, `3`). No incluye
  un parser genérico que permita al usuario escribir cualquier expresión
  booleana en tiempo de ejecución.
- Solo se manejan 3 variables (A, B, C); el enunciado menciona también
  una posible variable D, que no se usa en las 3 expresiones elegidas
  para este taller, pero el patrón de `generar_tabla_verdad` se podría
  extender fácilmente a 4 variables (`2^4 = 16` filas) si fuera necesario.
- La evaluación de una entrada concreta solo pide valores para A, B, C;
  no valida entradas fuera de esas tres variables.