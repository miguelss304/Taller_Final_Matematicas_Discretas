def ingresar_notas(x):

    notas = []
    print ("Ingrese las notas (de 0 a 50):")
    for i in range(x):
        while True:
            nota = int(input(f"Nota{i + 1}: "))
            if 0 <= nota <= 50:
                notas.append(nota)
                break
            else:
                print("Nota inválida. Por favor, ingrese una nota del 0 al 50.")
    return notas