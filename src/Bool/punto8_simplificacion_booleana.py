"""
Simplificación booleana: algoritmo de Quine-McCluskey
========================================================

Recibe una función booleana definida por sus minterminos (suma de
productos) y produce una expresión equivalente pero más simple, con
menos literales y por lo tanto menos compuertas.

Idea matemática:
    Un mintermino es un producto (AND) de todas las variables, cada una
    en su forma normal o negada, que vale 1 para exactamente UNA
    combinación de entrada. El número decimal del mintermino, escrito en
    binario, es justamente esa combinación (ej: con A,B,C -> mintermino
    5 = 101 = A.B'.C).

    Dos términos binarios se pueden combinar si difieren en un solo bit;
    esa posición se reemplaza por un guión, indicando que esa variable
    ya no afecta el resultado. Repitiendo este proceso se obtienen los
    implicantes primos: términos que ya no se pueden simplificar más.

    Dos expresiones booleanas son equivalentes si y solo si tienen la
    misma tabla de verdad, sin importar qué tan distintas se vean
    algebraicamente. Por eso el programa verifica el resultado
    recorriendo las 2^n combinaciones de entrada posibles.

Estructura del archivo:
    1. Utilidades básicas (conversión a binario, combinación de términos).
    2. Algoritmo de Quine-McCluskey (obtención de implicantes primos).
    3. Selección de implicantes (tabla de cobertura).
    4. Traducción de términos binarios a expresión algebraica.
    5. Verificación por tabla de verdad.
    6. Entrada de datos por consola (validación incluida).
    7. Programa principal.
"""


# ---------------------------------------------------------------------------
# 1. Utilidades básicas
# ---------------------------------------------------------------------------
def a_binario(numero, num_variables):
    """Convierte un mintermino decimal a su representación binaria de
    longitud fija (num_variables bits)."""
    return format(numero, f'0{num_variables}b')


def combinar_terminos(bits1, bits2):
    """
    Intenta combinar dos términos binarios (pueden tener guiones '-').

    Se pueden combinar únicamente si difieren en exactamente una
    posición (los guiones también cuentan como carácter, así que deben
    estar alineados). Si se pueden combinar, retorna el término
    resultante con esa posición marcada como '-'; si no, retorna None.
    """
    diferencias = 0
    posicion = -1
    for i in range(len(bits1)):
        if bits1[i] != bits2[i]:
            diferencias += 1
            posicion = i
            if diferencias > 1:
                return None
    if diferencias == 1:
        return bits1[:posicion] + '-' + bits1[posicion + 1:]
    return None


# ---------------------------------------------------------------------------
# 2. Algoritmo de Quine-McCluskey: obtención de implicantes primos
# ---------------------------------------------------------------------------
def obtener_implicantes_primos(minterminos, num_variables):
    """
    Aplica el algoritmo de Quine-McCluskey y retorna el conjunto de
    implicantes primos.

    Cada implicante primo es una tupla (bits_con_guiones, minterminos
    que cubre). En cada ronda se agrupan los términos por su cantidad de
    unos y se intenta combinar cada término con los del grupo siguiente;
    los que no logran combinarse ya no se pueden simplificar más y pasan
    a ser implicantes primos. El proceso se repite hasta que no queden
    combinaciones posibles.
    """
    terminos = [(a_binario(m, num_variables), frozenset([m])) for m in minterminos]
    implicantes_primos = set()

    while terminos:
        grupos = {}
        for bits, cubiertos in terminos:
            unos = bits.count('1')
            grupos.setdefault(unos, []).append((bits, cubiertos))

        claves_ordenadas = sorted(grupos.keys())
        nuevos_terminos = []
        usados = set()

        for i in range(len(claves_ordenadas) - 1):
            grupo_actual = grupos[claves_ordenadas[i]]
            grupo_siguiente = grupos[claves_ordenadas[i + 1]]

            for bits1, cub1 in grupo_actual:
                for bits2, cub2 in grupo_siguiente:
                    combinado = combinar_terminos(bits1, bits2)
                    if combinado is not None:
                        nuevo = (combinado, cub1 | cub2)
                        if nuevo not in nuevos_terminos:
                            nuevos_terminos.append(nuevo)
                        usados.add((bits1, cub1))
                        usados.add((bits2, cub2))

        for termino in terminos:
            if termino not in usados:
                implicantes_primos.add(termino)

        terminos = nuevos_terminos

    return implicantes_primos


# ---------------------------------------------------------------------------
# 3. Selección de implicantes: tabla de cobertura
# ---------------------------------------------------------------------------
def seleccionar_implicantes(implicantes_primos, minterminos):
    """
    Elige el subconjunto mínimo de implicantes primos que cubre todos
    los minterminos originales.

    Primero se toman los implicantes esenciales: aquellos que son la
    única opción que cubre algún mintermino en particular. Si después de
    eso quedan minterminos sin cubrir, se completan con un criterio
    goloso, eligiendo en cada paso el implicante que cubra más
    minterminos faltantes (suficiente para funciones de 3-4 variables).
    """
    cobertura = {m: [] for m in minterminos}
    for imp in implicantes_primos:
        for m in imp[1]:
            cobertura[m].append(imp)

    seleccionados = set()
    for m, imps in cobertura.items():
        if len(imps) == 1:
            seleccionados.add(imps[0])

    cubiertos = set()
    for imp in seleccionados:
        cubiertos |= imp[1]

    faltantes = set(minterminos) - cubiertos
    candidatos = [imp for imp in implicantes_primos if imp not in seleccionados]

    while faltantes:
        mejor = max(candidatos, key=lambda imp: len(imp[1] & faltantes))
        seleccionados.add(mejor)
        faltantes -= mejor[1]
        candidatos.remove(mejor)

    return seleccionados


# ---------------------------------------------------------------------------
# 4. Traducción de términos binarios a expresión algebraica
# ---------------------------------------------------------------------------
def termino_a_expresion(bits, nombres_variables):
    """Convierte una cadena de bits (con posibles guiones) en un producto
    de literales: '1' -> variable normal, '0' -> variable negada,
    '-' -> la variable se omite (fue eliminada al simplificar)."""
    literales = []
    for bit, var in zip(bits, nombres_variables):
        if bit == '1':
            literales.append(var)
        elif bit == '0':
            literales.append(var + "'")
    return ''.join(literales) if literales else '1'


def expresion_final(seleccionados, nombres_variables):
    """Une los términos seleccionados con OR para formar la expresión final."""
    terminos_expr = [termino_a_expresion(bits, nombres_variables)
                      for bits, _ in seleccionados]
    return ' + '.join(sorted(terminos_expr))


# ---------------------------------------------------------------------------
# 5. Verificación por tabla de verdad
# ---------------------------------------------------------------------------
def verificar_equivalencia(minterminos, seleccionados, num_variables, nombres_variables):
    """
    Recorre las 2^n combinaciones de entrada posibles y compara, fila
    por fila, el resultado de la función original (definida por la lista
    de minterminos) contra el resultado de la expresión simplificada. Si
    coinciden en todas las filas, ambas expresiones tienen la misma
    tabla de verdad y por lo tanto son equivalentes.
    """
    for combinacion in range(2 ** num_variables):
        bits_entrada = a_binario(combinacion, num_variables)
        valores = {var: int(bit) for var, bit in zip(nombres_variables, bits_entrada)}

        resultado_original = 1 if combinacion in minterminos else 0

        resultado_simplificado = 0
        for bits, _ in seleccionados:
            valor_termino = 1
            for bit, var in zip(bits, nombres_variables):
                if bit == '1' and valores[var] == 0:
                    valor_termino = 0
                    break
                if bit == '0' and valores[var] == 1:
                    valor_termino = 0
                    break
            resultado_simplificado |= valor_termino

        if resultado_original != resultado_simplificado:
            return False, combinacion

    return True, None


def simplificar(minterminos, num_variables, nombres_variables=None):
    """Ejecuta el proceso completo: obtiene los implicantes primos, elige
    el subconjunto mínimo, arma la expresión final y la verifica contra
    la tabla de verdad original."""
    if nombres_variables is None:
        nombres_variables = ['A', 'B', 'C', 'D'][:num_variables]

    implicantes_primos = obtener_implicantes_primos(minterminos, num_variables)
    seleccionados = seleccionar_implicantes(implicantes_primos, minterminos)
    expresion = expresion_final(seleccionados, nombres_variables)
    equivalente, fallo = verificar_equivalencia(
        minterminos, seleccionados, num_variables, nombres_variables
    )

    return {
        'expresion': expresion,
        'implicantes_primos': implicantes_primos,
        'implicantes_seleccionados': seleccionados,
        'equivalente': equivalente,
        'combinacion_fallida': fallo,
    }


# ---------------------------------------------------------------------------
# 6. Entrada de datos por consola (validación incluida)
# ---------------------------------------------------------------------------
def pedir_numero_variables():
    """Pide el número de variables de la función booleana (solo se admiten 3 o 4)."""
    numero = int(input("Ingrese el número de variables (3 o 4): "))
    while numero not in (3, 4):
        print("Solo se admiten funciones de 3 o 4 variables.")
        numero = int(input("Ingrese el número de variables (3 o 4): "))
    return numero


def pedir_minterminos(num_variables):
    """Pide la lista de minterminos, validando que estén en el rango
    válido (0 a 2^n - 1) y que no haya repetidos."""
    maximo = 2 ** num_variables - 1
    print(f"Ingrese los minterminos (enteros de 0 a {maximo}, separados por espacios):")
    while True:
        valores = input("Minterminos: ").split()
        try:
            minterminos = [int(v) for v in valores]
        except ValueError:
            print("Todos los valores deben ser números enteros.")
            continue
        if not minterminos:
            print("Debe ingresar al menos un mintermino.")
        elif any(m < 0 or m > maximo for m in minterminos):
            print(f"Todos los minterminos deben estar entre 0 y {maximo}.")
        elif len(set(minterminos)) != len(minterminos):
            print("No se permiten minterminos repetidos.")
        else:
            return sorted(set(minterminos))


# ---------------------------------------------------------------------------
# 7. Programa principal
# ---------------------------------------------------------------------------
def mostrar_resultado(minterminos, num_variables, nombres_variables):
    """Imprime los implicantes primos, la expresión simplificada y el
    resultado de la verificación contra la tabla de verdad."""
    resultado = simplificar(minterminos, num_variables, nombres_variables)

    print(f"\nMinterminos: {minterminos}")
    print(f"Variables: {nombres_variables}\n")

    print("Implicantes primos encontrados:")
    for bits, cubiertos in resultado['implicantes_primos']:
        expr = termino_a_expresion(bits, nombres_variables)
        print(f"  {bits}  ->  {expr:6s}  (cubre minterminos {sorted(cubiertos)})")

    print(f"\nExpresión simplificada: {resultado['expresion']}")
    print(f"¿Misma tabla de verdad que la original? {resultado['equivalente']}")
    if not resultado['equivalente']:
        print(f"  Falla en la combinación: {resultado['combinacion_fallida']}")


def main():
    num_variables = pedir_numero_variables()
    minterminos = pedir_minterminos(num_variables)
    nombres_variables = ['A', 'B', 'C', 'D'][:num_variables]
    mostrar_resultado(minterminos, num_variables, nombres_variables)


if __name__ == "__main__":
    main()