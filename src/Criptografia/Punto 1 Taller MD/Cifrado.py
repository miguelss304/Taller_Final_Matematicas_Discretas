from PosicionNueva import nueva_posicion
def cifrar_mensaje():
    x = str(input("Ingrese el mensaje a cifrar: "))
    texto = x.upper()
    k = int(input("Ingrese el valor de k: ")) #Se pide la posicion y cuanto desplazamiento quiero realizar

    abecedario = nueva_posicion(k)
    for letra in texto:
        if letra in abecedario:
            letra = abecedario[letra]
            print (letra, end="")
        else:
            print (letra, end="") #Se realiza el cifrado del mensaje, si la letra no esta en el abecedario se imprime tal cual