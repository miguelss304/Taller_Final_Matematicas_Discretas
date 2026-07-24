from PosicionVieja import vieja_posicion
def descifrar_mensaje():
    x = str(input("Ingrese el mensaje a descifrar: "))
    texto = x.upper()
    k = int(input("Ingrese el valor de k: ")) #Se pude la posicion y cuanto desplazamiento quiero realizar

    abecedario = vieja_posicion(k)
    for letra in texto:
        if letra in abecedario:
            letra = abecedario[letra]
            print (letra, end="")
        else:
            print (letra, end="")