def contar_letras(texto):
    letras = {} # Esto es un diccionario, que almacena tanto la letra como el numero de veces que aparece
    
    for x in texto:
        if x in letras: # Verifica si la letra ya esta almacenada dentro de nuestro diccionario
            letras[x] = letras[x] + 1 # Busca la clave de la letra y a su "atributo" le suma 1
        else:
            letras[x] = 1 # Si no esta almacenada la clave, la agrega y le asigna un valor de 1

    return letras # Retorna el diccionario con las letras y su numero de apariciones