from Dividir import dividir_notas
def repartir_notas(notas, M):
    servidor1 = []
    servidor2 = []
    servidor3 = []

    for x in notas:
        s1, s2, s3 = dividir_notas(x, M)
        servidor1.append(s1)
        servidor2.append(s2)
        servidor3.append(s3)
    return servidor1, servidor2, servidor3