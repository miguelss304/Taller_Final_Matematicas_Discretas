# Taller 3 — Programación discreta

**Universidad Nacional de Colombia — Matemáticas Discretas I**
Criptografía, grafos, álgebra de Boole, Shannon y un primer vistazo cuántico.

## Integrantes

- Miguel Angel Sanchez Sandoval
- David Montiel

## Lenguaje usado

Python 3.8+. No se usan librerías externas más allá de la biblioteca
estándar (`heapq`, `math`, `random`, `copy`, etc.), salvo que se indique lo
contrario en el punto correspondiente.

## Estructura del repositorio

```
.
├── README.md
├── requirements.txt
├── src/
│   ├── Criptografia/         # Puntos 1-3
│   │   ├── punto1_cesar.py
│   │   ├── punto2_RSA.py
│   │   └── punto3_MPC.py
│   ├── Grafos/                # Puntos 4-5
│   │   ├── punto4_dijkstra/
│   │   │   ├── dijkstra.py
│   │   │   ├── ejecutar_grafo.py
│   │   │   └── grafo_ciudad.txt
│   │   └── punto5_cierre_estacion.py
│   ├── Bool/                   # Puntos 6-8
│   └── Cuantica/               # Puntos 9-10
│       └── punto9_shannon.py
├── tests/                      # Pruebas de cada punto (test_*.py)
└── docs/                       # Documentación matemática de cada punto (un .md por punto)
```

## Cómo ejecutar el proyecto

Cada punto es independiente y se ejecuta por separado.

**Ejecutar la demostración de un punto** (pararse en la carpeta que
contiene el archivo, si depende de rutas relativas como el grafo del
Punto 4):

```bash
python src/<bloque>/<archivo>.py
```

**Ejecutar las pruebas de un punto** (desde la raíz del repositorio):

```bash
python -m tests.test_<nombre>
# o, si se tiene pytest instalado:
pytest tests/test_<nombre>.py -v
```

## Lista de ejercicios desarrollados

| # | Punto | Estado | Código | Pruebas | Documentación |
|---|-------|--------|--------|---------|----------------|
| 1 | Cifrado César | ✅ Completo | `src/Criptografia/punto1_cesar.py` | `tests/test_1_cesar.py` | `docs/punto1_cesar.md` |
| 2 | RSA de juguete | ✅ Completo | `src/Criptografia/punto2_RSA.py` | `tests/test_2_RSA.py` | `docs/punto2_RSA.md` |
| 3 | MPC básico | ✅ Completo | `src/Criptografia/punto3_MPC.py` | `tests/test_3_MPC.py` | `docs/punto3_MCP.md`* |
| 4 | Ruta más corta (Dijkstra) | ✅ Completo | `src/Grafos/punto4_dijkstra/dijkstra.py` | `tests/test_4_dijkstra.py` | `docs/punto4_dijkstra.md` |
| 5 | Cierre de una estación | ✅ Completo | `src/Grafos/punto5_cierre_estacion.py` | `tests/test_5_cierre_estacion.py` | `docs/punto5_cierre_estacion.md` |
| 6 | Coloreo de grafos | ⬜ Pendiente | `src/Bool/` | `tests/` | `docs/` |
| 7 | Tablas de verdad | ⬜ Pendiente | `src/Bool/` | `tests/` | `docs/` |
| 8 | Simplificación booleana | ⬜ Pendiente | `src/Bool/` | `tests/` | `docs/` |
| 9 | Entropía de Shannon | ✅ Completo | `src/Cuantica/punto9_shannon.py` | `tests/test_9_shannon.py` | `docs/punto9_shannon.md` |
| 10 | Simulador de un qubit | ⬜ Pendiente | `src/Cuantica/` | `tests/` | `docs/` |


## requirements.txt

No se requieren librerías externas para ningún punto completado hasta el
momento. Se usa únicamente la biblioteca estándar de Python (`heapq`,
`math`, `random`, `copy`).