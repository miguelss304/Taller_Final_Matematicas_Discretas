# Taller 3 — Programación discreta

**Universidad Nacional de Colombia — Matemáticas Discretas I**
Criptografía, grafos, álgebra de Boole, Shannon y un primer vistazo cuántico.

## Integrantes

- Miguel Angel Sanchez Sandoval
- David Santiago Montiel Rodriguez

## Declaración de uso de IA

En el desarrollo de este taller se utilizó inteligencia artificial (IA)
como herramienta de apoyo, de la siguiente manera:

- **README:** este documento fue redactado casi en su totalidad con
  ayuda de IA, a partir de la información real del repositorio.
- **Código de cada punto:** primero se implementó la lógica y el
  algoritmo de cada punto por cuenta propia; después, ese código se pasó
  por una IA para darle formato, organizarlo mejor y redactar los
  comentarios ya hechos de forma más clara.
- **Documentación de cada punto (`docs/`):** se siguió el mismo proceso:
  las explicaciones matemáticas y conceptuales se redactaron primero por
  nuestra parte, y luego se usó IA como apoyo para mejorar la gramática y
  la redacción.
- **Pruebas (`tests/`):** se usó IA como apoyo principal para escribir
  los archivos de test, ya que no contábamos con experiencia previa
  usando frameworks de pruebas como `pytest`.

## Lenguaje usado

Python 3.8+. No se usan librerías externas más allá de la biblioteca
estándar (`heapq`, `math`, `random`, `copy`, `cmath`, `itertools`), salvo
que se indique lo contrario en el punto correspondiente.

## Estructura del repositorio

```
.
├── README.md
├── requirements.txt
├── src/
│   ├── Criptografia/                  # Puntos 1-3
│   │   ├── punto1_cesar.py
│   │   ├── punto2_RSA.py
│   │   └── punto3_MPC.py
│   ├── Grafos/                         # Puntos 4-6
│   │   ├── punto4_dijkstra/
│   │   │   ├── dijkstra.py
│   │   │   ├── ejecutar_grafo.py
│   │   │   └── grafo_ciudad.txt
│   │   ├── punto5_cierre_estacion.py
│   │   └── punto6_coloreo_grafos.py
│   ├── Bool/                            # Puntos 7-8
│   │   ├── punto7_tablas_verdad.py
│   │   └── punto8_simplificacion_booleana.py
│   └── Cuantica/                        # Puntos 9-10
│       ├── punto9_shannon.py
│       └── punto10_qubit.py
├── tests/                                # Pruebas de cada punto (test_*.py)
└── docs/                                 # Documentación matemática de cada punto (un .md por punto)
```

## Cómo ejecutar el proyecto

Cada punto es independiente y se ejecuta por separado.

**Ejecutar la demostración de un punto** (pararse en la carpeta que
contiene el archivo, si depende de rutas relativas como el grafo del
Punto 4):

```bash
python src/<bloque>/<archivo>.py
```

**Ejecutar las pruebas de un solo punto** (desde la raíz del repositorio):

```bash
python -m tests.test_<nombre>
# o, si se tiene pytest instalado:
pytest tests/test_<nombre>.py -v
```

**Ejecutar TODAS las pruebas del taller de una sola vez:**

```bash
pytest tests/ -v
```

Esto descubre y corre automáticamente los 10 archivos `test_*.py` de la
carpeta `tests/`. Cada test inserta en `sys.path` la ruta a su propio
módulo (con nombres de archivo únicos entre puntos), por lo que no hay
conflictos de importación al correrlos todos juntos en la misma sesión.

## Lista de ejercicios desarrollados

| # | Punto | Estado | Código | Pruebas | Documentación |
|---|-------|--------|--------|---------|----------------|
| 1 | Cifrado César | ✅ Completo | `src/Criptografia/punto1_cesar.py` | `tests/test_1_cesar.py` | `docs/punto1_cesar.md` |
| 2 | RSA de juguete | ✅ Completo | `src/Criptografia/punto2_RSA.py` | `tests/test_2_RSA.py` | `docs/punto2_RSA.md` |
| 3 | MPC básico | ✅ Completo | `src/Criptografia/punto3_MPC.py` | `tests/test_3_MPC.py` | `docs/punto3_MPC.md` |
| 4 | Ruta más corta (Dijkstra) | ✅ Completo | `src/Grafos/punto4_dijkstra/dijkstra.py` | `tests/test_4_dijkstra.py` | `docs/punto4_dijkstra.md` |
| 5 | Cierre de una estación | ✅ Completo | `src/Grafos/punto5_cierre_estacion.py` | `tests/test_5_cierre_estacion.py` | `docs/punto5_cierre_estacion.md` |
| 6 | Coloreo de grafos | ✅ Completo | `src/Grafos/punto6_coloreo_grafos.py` | `tests/test_6_coloreo_grafos.py` | `docs/punto6_coloreo_grafos.md` |
| 7 | Tablas de verdad | ✅ Completo | `src/Bool/punto7_tablas_verdad.py` | `tests/test_7_tablas_verdad.py` | `docs/punto7_tablas_verdad.md` |
| 8 | Simplificación booleana | ✅ Completo | `src/Bool/punto8_simplificacion_booleana.py` | `tests/test_8_simplificacion_booleana.py` | `docs/punto8_simplificacion_booleana.md` |
| 9 | Entropía de Shannon | ✅ Completo | `src/Cuantica/punto9_shannon.py` | `tests/test_9_shannon.py` | `docs/punto9_shannon.md` |
| 10 | Simulador de un qubit | ✅ Completo | `src/Cuantica/punto10_qubit.py` | `tests/test_10_qubit.py` | `docs/punto10_qubit.md` |

## requirements.txt

No se requieren librerías externas para ningún punto del taller. Se usa
únicamente la biblioteca estándar de Python (`heapq`, `math`, `random`,
`copy`, `cmath`, `itertools`). Se recomienda tener `pytest` instalado
para ejecutar las pruebas con `pytest tests/ -v`, aunque cada archivo de
pruebas también puede correrse directamente con `python` sin pytest.
