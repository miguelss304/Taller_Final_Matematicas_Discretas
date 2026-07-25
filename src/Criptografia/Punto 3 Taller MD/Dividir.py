import random
def dividir_notas(x, M):
    s1 = random.randint(0, M-1)
    s2 = random.randint(0, M-1)
    s3 = (x -s1 - s2) % M
    return s1, s2, s3