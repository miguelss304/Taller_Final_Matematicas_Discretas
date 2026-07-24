from Posicion import nueva_posicion
x = str(input("Ingrese el mensaje a cifrar: "))
texto = x.upper()
k = int(input("Ingrese el valor de k: "))

abecedario = nueva_posicion(k)
for letra in texto:
    if letra in abecedario:
        letra = abecedario[letra]
        print (letra, end="")
    else:
        print (letra, end="")