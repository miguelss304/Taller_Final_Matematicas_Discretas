# Punto 2 — RSA de juguete: llaves, cifrado y descifrado

## 1. ¿Qué problema resuelve el programa?

El programa implementa una versión reducida del algoritmo RSA, uno de los
cifrados de clave pública más usados en la práctica, con el fin de
entender su idea matemática. A partir de dos números primos `p, q` y un
exponente público `e`, el programa calcula todo lo necesario para cifrar y
descifrar un mensaje numérico `M`:

- el módulo `n = p·q`;
- la función de Euler `φ(n) = (p-1)(q-1)`;
- el exponente privado `d`, inverso modular de `e` módulo `φ(n)`;
- el cifrado `C ≡ M^e (mód n)`;
- el descifrado `M ≡ C^d (mód n)`.

**Importante:** esta es una versión de juguete, con primos pequeños. No
debe presentarse ni usarse como una implementación de seguridad real.

## 2. ¿Qué idea matemática usa?

### El papel de los primos

RSA se apoya en una asimetría matemática: es fácil multiplicar dos primos
grandes `p` y `q` para obtener `n = p·q`, pero es computacionalmente muy
difícil hacer el proceso inverso (factorizar `n` para recuperar `p` y `q`)
cuando los primos son suficientemente grandes. Esa dificultad de
factorización es la que en teoría protege la clave privada en un RSA real.
Además, conocer `p` y `q` es justamente lo que permite calcular
`φ(n) = (p-1)(q-1)`, que es indispensable para encontrar el exponente
privado `d`. Sin conocer los primos originales (solo conociendo `n`), no
se puede calcular `φ(n)` de forma directa.

### El papel del inverso modular

El cifrado y el descifrado son operaciones inversas entre sí gracias a
que `e` y `d` se eligen para que cumplan:

```
(e · d) ≡ 1 (mód φ(n))
```

Esta relación (garantizada por el teorema de Euler) hace que:

```
(M^e)^d ≡ M^(e·d) ≡ M^(k·φ(n) + 1) ≡ M (mód n)
```

para cierto entero `k`. Es decir, elevar el mensaje cifrado a la potencia
`d` "deshace" exactamente el efecto de haberlo elevado a la potencia `e`.
El inverso modular `d` se calcula con el **algoritmo de Euclides
extendido**, que además de calcular el máximo común divisor entre dos
números, encuentra los coeficientes `x, y` de la identidad de Bézout:

```
e·x + φ(n)·y = gcd(e, φ(n))
```

Cuando `gcd(e, φ(n)) = 1` (condición necesaria para que exista el
inverso), el coeficiente `x` de esa identidad es directamente el inverso
modular de `e` (ajustado al rango `[0, φ(n)-1]`).

### El papel de la congruencia

Todas las operaciones de RSA (cifrado, descifrado, cálculo del inverso)
se hacen dentro de la aritmética modular: los resultados no son los
números reales de las potencias `M^e` o `C^d` (que serían enormes), sino
sus **restos módulo `n`**. Esto es lo que hace viable el cálculo incluso
con exponentes grandes, usando exponenciación modular eficiente
(`pow(base, exponente, modulo)` en Python calcula esto sin necesitar
construir el número gigante intermedio).

## 3. ¿Cómo se ejecuta?

Requisitos: Python 3.8+. No se usan librerías externas.

**Ejecutar el programa interactivo:**

```bash
cd "src/Criptografia/Punto 2 Taller MD"
python rsa.py
```

**Ejemplo (caso de prueba obligatorio del taller):**

```
Ingrese el primo p: 61
Ingrese el primo q: 53
Ingrese el exponente público e: 17
n = 3233
phi(n) = 3120
d = 2753
Ingrese el mensaje M a cifrar (número entero): 65
Cifrado: C = 2790
Descifrado: M = 65
```

**Usar las funciones puras desde otro script:**

```python
from rsa import generar_llaves, cifrar, descifrar

n, phi_n, d = generar_llaves(p=61, q=53, e=17)
C = cifrar(65, e=17, n=n)          # -> 2790
M = descifrar(C, d=d, n=n)          # -> 65
```

**Ejecutar las pruebas:**

```bash
python -m tests.test_2_rsa
# o
pytest tests/test_2_rsa.py -v
```

## 4. ¿Qué pruebas hicieron?

El archivo `tests/test_2_rsa.py` contiene 6 casos:

| # | Caso | Entrada | Salida esperada |
|---|------|---------|------------------|
| 1 | Caso obligatorio del taller | p=61, q=53, e=17, M=65 | n=3233, φ(n)=3120, d=2753, C=2790, M recuperado=65 |
| 2 | Euclides extendido (gcd + Bézout) | a=17, b=3120 | gcd=1 y se cumple `17x + 3120y = 1` |
| 3 | Inverso modular correcto | e=17, φ=3120 | `(e·d) mod φ = 1` |
| 4 | e inválido | p=61, q=53, e=2 (gcd(2,3120)=2) | lanza `ValueError` |
| 5 | Cifrar+descifrar = identidad | p=7, q=11, e=7, M=5 | recupera M=5 |
| 6 | n y φ(n) correctos | p=7, q=11 | n=77, φ(n)=60 |

Todos los casos pasan correctamente al día de esta entrega.

## 5. ¿Qué limitaciones tiene la solución?

- Se usan primos pequeños ingresados manualmente; el programa no verifica
  que `p` y `q` sean realmente primos ni que sean lo suficientemente
  grandes para ofrecer seguridad real.
- No se implementa ningún esquema de *padding* (como OAEP), que en RSA
  real es indispensable para evitar ataques que explotan la estructura
  matemática pura del cifrado determinista.
- El mensaje `M` debe ser un número entero menor que `n`; el programa no
  incluye la conversión de texto a números (esa transformación quedaría
  fuera del alcance de este ejercicio educativo).
- Como se aclara en el enunciado, esta implementación es exclusivamente
  para fines didácticos y no debe usarse para proteger información
  sensible real.