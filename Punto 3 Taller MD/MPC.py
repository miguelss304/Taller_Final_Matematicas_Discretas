from Notas import ingresar_notas
from Repartir import repartir_notas
from Reconstruir import reconstruir_nota, suma_servidor
x = int(input("Ingrese el total de notas a ingresar: "))
while x <= 0:
    print("El número de notas debe ser mayor que cero.")
    x = int(input("Ingrese el total de notas a ingresar: "))

M = 1000003
notas = ingresar_notas(x)
servidor1, servidor2, servidor3 = repartir_notas(notas, M)

S1 = suma_servidor(servidor1, M) 
S2 = suma_servidor(servidor2, M)
S3 = suma_servidor(servidor3, M)

suma_total, promedio = reconstruir_nota(S1, S2, S3, M, x)

print(f"Suma total de las notas: {suma_total}")
print(f"Promedio de las notas: {promedio}")
