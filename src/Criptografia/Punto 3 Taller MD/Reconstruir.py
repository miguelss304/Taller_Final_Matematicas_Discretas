def suma_servidor(lista_partes,M):
    return sum(lista_partes) % M

def reconstruir_nota(S1, S2, S3, M, x):
    suma_total = (S1 + S2 + S3) % M
    promedio = suma_total // x
    return suma_total, promedio