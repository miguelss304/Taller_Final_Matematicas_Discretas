from Notas import ingresar_notas
x = int(input("Ingrese el total de notas a ingresar: "))
while x <= 0:
    print("El número de notas debe ser mayor que cero.")
    x = int(input("Ingrese el total de notas a ingresar: "))
notas = ingresar_notas(x)
