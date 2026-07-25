from Cifrado import cifrar_mensaje
from Descifrado import descifrar_mensaje
x = int(input("Ingrese si desea cifrar o descifrar el mensaje: \n 1. Cifrar \n 2. Descifrar \n"))
if x == 1:
    cifrar_mensaje()
elif x == 2:
    descifrar_mensaje()
#Funciona como main para que el usuario escoja que desea