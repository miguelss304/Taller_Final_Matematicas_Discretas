"""
RSA de juguete: llaves, cifrado y descifrado
===============================================

Versión reducida de RSA, solo para entender la idea matemática detrás del
cifrado de clave pública. NO debe usarse como seguridad real: usa primos
pequeños y no incluye ninguna de las protecciones necesarias en una
implementación de producción (padding, primos grandes, etc.).

Idea matemática:
    1. Se eligen dos primos p, q y se calcula n = p*q (el módulo público).
    2. Se calcula φ(n) = (p-1)(q-1) (la función de Euler para n).
    3. Se elige un exponente público e tal que gcd(e, φ(n)) = 1, y se
       calcula su inverso modular d, tal que (e * d) ≡ 1 (mód φ(n)).
    4. Cifrar:    C ≡ M^e (mód n)
       Descifrar: M ≡ C^d (mód n)

Estructura del archivo:
    1. Algoritmo de Euclides extendido (para inversos modulares y gcd).
    2. Cálculo de las llaves (n, φ(n), d) a partir de p, q, e.
    3. Cifrado y descifrado.
    4. Entrada de datos por consola.
"""


# ---------------------------------------------------------------------------
# 1. Algoritmo de Euclides extendido
# ---------------------------------------------------------------------------
def euclides_extendido(a, b):
    """
    Calcula el máximo común divisor de (a, b) y los coeficientes de
    Bézout (x, y) tales que:
        a*x + b*y = gcd(a, b)

    Devuelve la tupla (gcd, x, y).

    Se usa para encontrar el inverso modular: si gcd(e, phi) = 1, el
    coeficiente x de esta identidad es exactamente el inverso de e
    módulo phi (ver inverso_modular más abajo).
    """
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = euclides_extendido(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def inverso_modular(e, phi):
    """
    Calcula el inverso modular d de e módulo phi, es decir, el número d
    tal que (e * d) % phi == 1.

    Lanza ValueError si e no tiene inverso módulo phi, lo cual ocurre
    exactamente cuando gcd(e, phi) != 1 (e y phi no son primos entre sí).
    """
    gcd, x, _ = euclides_extendido(e, phi)

    if gcd != 1:
        raise ValueError(
            f"e={e} no es válido: gcd(e, phi(n))={gcd} (debe ser 1). "
            "Elija otro exponente público e."
        )

    # x puede salir negativo; se normaliza al rango [0, phi-1]
    return x % phi


# ---------------------------------------------------------------------------
# 2. Cálculo de las llaves a partir de p, q, e
# ---------------------------------------------------------------------------
def generar_llaves(p, q, e):
    """
    Calcula n, phi(n) y el exponente privado d a partir de dos primos
    p, q y un exponente público e.

    Devuelve la tupla (n, phi_n, d).
    """
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = inverso_modular(e, phi_n)
    return n, phi_n, d


# ---------------------------------------------------------------------------
# 3. Cifrado y descifrado
# ---------------------------------------------------------------------------
def cifrar(M, e, n):
    """Cifra un mensaje numérico M: C ≡ M^e (mód n)."""
    return pow(M, e, n)


def descifrar(C, d, n):
    """Descifra un mensaje cifrado C: M ≡ C^d (mód n)."""
    return pow(C, d, n)


# ---------------------------------------------------------------------------
# 4. Programa principal (entrada de datos por consola)
# ---------------------------------------------------------------------------
def main():
    p = int(input("Ingrese el primo p: "))
    q = int(input("Ingrese el primo q: "))
    e = int(input("Ingrese el exponente público e: "))

    try:
        n, phi_n, d = generar_llaves(p, q, e)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(f"n = {n}")
    print(f"phi(n) = {phi_n}")
    print(f"d = {d}")

    M = int(input("Ingrese el mensaje M a cifrar (número entero): "))
    C = cifrar(M, e, n)
    print(f"Cifrado: C = {C}")

    M_recuperado = descifrar(C, d, n)
    print(f"Descifrado: M = {M_recuperado}")


if __name__ == "__main__":
    main()