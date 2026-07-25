def  vieja_posicion(k):
    abecedario = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    new_abecedario = {}
    for clave, valor in abecedario.items():
        posicion_nueva  = (valor - k) % 26
        new_abecedario[clave] = letras[posicion_nueva]
    return new_abecedario
#Se crea un nuevo diccionario que contenga las nuevas posiciones de las letras del abecedario  