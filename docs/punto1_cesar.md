# Punto 1 — Cifrado César: romper un mensaje antiguo

## 1. ¿Qué problema resuelve el programa?

El programa implementa el cifrado César, uno de los métodos de cifrado más
antiguos conocidos. Permite:

- **Cifrar** un texto desplazando cada letra `k` posiciones hacia adelante
  en el alfabeto.
- **Descifrar** un texto cifrado, si se conoce el desplazamiento `k`,
  desplazando las letras la misma cantidad pero hacia atrás.
- **Romper** un mensaje cifrado cuando no se conoce `k`, probando los 26
  desplazamientos posibles (ataque de fuerza bruta) y dejando que el usuario
  identifique cuál resultado tiene sentido en español.

Se conservan espacios, signos de puntuación y números tal cual aparecen en
el texto original; solo las letras del alfabeto se transforman.

## 2. ¿Qué idea matemática usa?

El cifrado César es un caso particular de **aritmética modular**. Cada letra
se identifica con un número entre `0` y `25` según su posición en el
alfabeto (A=0, B=1, ..., Z=25). Cifrar con desplazamiento `k` consiste en
aplicar la operación:

```
posición_cifrada = (posición_original + k) mod 26
```

Y descifrar consiste en aplicar la operación inversa:

```
posición_original = (posición_cifrada - k) mod 26
```

### ¿Por qué el descifrado usa el desplazamiento contrario?

Cifrar es una función que "rota" cada letra `k` posiciones hacia adelante en
un ciclo de 26 elementos (el módulo 26 hace que, al pasar de `Z`, se vuelva a
`A`). Para deshacer esa rotación y recuperar la letra original, es necesario
rotar exactamente la misma cantidad de posiciones, pero en sentido contrario.
Matemáticamente, sumar `k` y luego sumar `-k` (equivalente a restar `k`)
cancela el desplazamiento y devuelve la posición original:

```
(posición + k - k) mod 26 = posición mod 26 = posición
```

Esto es lo que hace la función `construir_tabla(k, direccion)`: con
`direccion=1` construye la tabla de cifrado (`+k`), y con `direccion=-1`
construye la tabla de descifrado (`-k`), reutilizando la misma lógica.

### ¿Por qué el ataque de fuerza bruta es posible en este cifrado?

El espacio de claves del cifrado César es extremadamente pequeño: solo hay
**26 desplazamientos posibles** (`k` puede ser `0, 1, 2, ..., 25`). Esto
significa que, sin conocer la clave, un atacante puede simplemente probar
los 26 valores de `k` uno por uno y revisar cuál de los 26 resultados
produce un texto con sentido en el idioma esperado (en este caso, español).

Este es precisamente el motivo por el cual el cifrado César **no se
considera seguro** para proteger información real: la cantidad de claves
posibles es tan reducida que probarlas todas toma una fracción de segundo,
incluso a mano. Un cifrado moderno necesita un espacio de claves
astronómicamente más grande para que la fuerza bruta sea inviable.

## 3. ¿Cómo se ejecuta?

Requisitos: Python 3.8+. No se usan librerías externas.

**Ejecutar el programa interactivo:**

```bash
cd "src/Criptografia/Punto 1 Taller MD"
python cesar.py
```

El programa muestra un menú:

```
Ingrese si desea cifrar o descifrar el mensaje:
 1. Cifrar
 2. Descifrar
 3. Probar todos los desplazamientos (fuerza bruta)
```

**Ejemplo (cifrar):**

```
Opción: 1
Mensaje: HOLA UNAL
k: 3
Mensaje cifrado: KROD XQDO
```

**Usar las funciones puras desde otro script:**

```python
from cesar import cifrar_texto, descifrar_texto

cifrado = cifrar_texto("HOLA UNAL", 3)      # -> "KROD XQDO"
original = descifrar_texto(cifrado, 3)       # -> "HOLA UNAL"
```

**Ejecutar las pruebas:**

```bash
python -m tests.test_1_cesar
# o
pytest tests/test_1_cesar.py -v
```

## 4. ¿Qué pruebas hicieron?

El archivo `tests/test_1_cesar.py` contiene 7 casos:

| # | Caso | Entrada | Salida esperada |
|---|------|---------|------------------|
| 1 | Cifrado (ejemplo del taller) | texto=`HOLA UNAL`, k=3 | `KROD XQDO` |
| 2 | Descifrado (inverso del anterior) | texto=`KROD XQDO`, k=3 | `HOLA UNAL` |
| 3 | Conserva caracteres no alfabéticos | texto=`HOLA, MUNDO 123!`, k=1 | `IPMB, NVOEP 123!` |
| 4 | Desplazamiento k=0 | texto=`PRUEBA`, k=0 | `PRUEBA` (sin cambios) |
| 5 | Desplazamiento que da la vuelta al alfabeto | texto=`XYZ`, k=3 | `ABC` |
| 6 | Cifrar + descifrar = identidad | texto largo, k=11 | recupera el texto original |
| 7 | La tabla de sustitución es una permutación válida | k=5 | 26 letras, sin repetidos |

Todos los casos pasan correctamente al día de esta entrega.

## 5. ¿Qué limitaciones tiene la solución?

- Solo soporta el alfabeto latino sin `Ñ` (A–Z), tal como pide el
  enunciado. Cualquier letra fuera de ese conjunto (incluida `Ñ` o letras
  con tilde) se trata como carácter no alfabético y se deja sin cambios.
- El texto se convierte siempre a mayúsculas antes de procesarlo; no se
  preserva la distinción entre mayúsculas y minúsculas del mensaje original.
- La fuerza bruta solo *muestra* las 26 posibilidades; no intenta decidir
  automáticamente cuál es la correcta (por ejemplo, mediante análisis de
  frecuencia de letras). Es el usuario quien identifica visualmente el
  resultado con sentido.
- Como se explica en la sección 2, el cifrado César no ofrece seguridad
  real: se incluye únicamente con fines educativos para ilustrar conceptos
  de aritmética modular y de espacio de claves pequeño.