def procesar_linea(linea):
    nombre = linea[:25].strip()
    icd10 = linea[25:31].strip()
    monto = int(linea[31:39].strip())
    alta_comp = len(linea) == 40 and linea[39] == "X"
    return nombre, icd10, monto, alta_comp

def redondear(numero, decimales):
    factor = 10 ** decimales
    return int(numero * factor + 0.5) / factor

def procesar_linea_especial(linea):
    monto_AL = int(linea[2:8].strip())
    monto_MZ = int(linea[8:14].strip())
    monto_U  = int(linea[16:22].strip())
    return monto_AL, monto_MZ, monto_U


def calcular_monto(monto_base, icd10, monto_AL, monto_MZ, monto_U, alta_comp):
    letra = icd10[0]

    # Adicional según letra
    if "A" <= letra <= "L":
        adicional = monto_AL
    elif letra == "U":
        adicional = monto_U
    else:  # M a Z sin U
        adicional = monto_MZ

    subtotal = monto_base + adicional

    # Porcentaje según número después del punto
    numero_post_punto = int(icd10.split(".")[1])  # <-- extrae el número después del punto
    subtotal = subtotal + subtotal * numero_post_punto / 100

    # Recargo alta complejidad
    if alta_comp:
        subtotal = subtotal * 1.05  # <-- 5% extra si es alta complejidad

    return subtotal


def principal():
    r1 = 0
    r2 = r3 = r4 = r5 = r6 = 0
    suma_cap19 = 0       # <-- para calcular promedio de capítulo 19
    cant_cap19 = 0
    mayor_monto = -1     # <-- para r8 y r9
    nombre_mayor = ""
    suma_total = 0       # <-- para el promedio general (r10)
    lista_alta_comp = [] # <-- para el segundo loop de r10

    monto_AL = monto_MZ = monto_U = 0  # <-- inicializados antes del loop

    m = open("tratamientos.txt", "rt")

    for linea in m:
        if linea[-1] == "\n":
            linea = linea[:-1]

        if linea[0] == "#":
            monto_AL, monto_MZ, monto_U = procesar_linea_especial(linea)

        else:
            nombre, icd10, monto_base, alta_comp = procesar_linea(linea)
            monto_final = calcular_monto(monto_base, icd10, monto_AL, monto_MZ, monto_U, alta_comp)

            r1 += 1  #  contamos tratamientos

            letra = icd10[0]
            if letra == "A": r2 += 1   #  contadores por letra
            elif letra == "B": r3 += 1
            elif letra == "C": r4 += 1
            elif letra == "E": r5 += 1
            elif letra == "P": r6 += 1

            # Capítulo 19: códigos que empiezan con S o T
            if letra in ("S", "T"):
                suma_cap19 += monto_final
                cant_cap19 += 1

            # Mayor monto (solo no-U)
            if letra != "U" and monto_final > mayor_monto:
                mayor_monto = monto_final
                nombre_mayor = nombre

            suma_total += monto_final  # acumulamos para promedio general

            if alta_comp:
                lista_alta_comp.append(monto_final)  #  guardamos para r10


    # Resultados intermedios
    r7 = redondear(suma_cap19 / cant_cap19, 2) if cant_cap19 > 0 else 0
    r8 = nombre_mayor
    r9 = redondear(mayor_monto, 2)

    promedio_general = suma_total / r1 if r1 > 0 else 0

    # Segundo loop para r10
    cant_alta_sobre_promedio = 0
    for monto in lista_alta_comp:
        if monto > promedio_general:
            cant_alta_sobre_promedio += 1

    r10 = int(cant_alta_sobre_promedio / len(lista_alta_comp) * 100) if lista_alta_comp else 0

    print('(r1) - Cantidad de tratamientos cargados:', r1)
    print('(r2) - Cantidad de tratamientos "A":', r2)
    print('(r3) - Cantidad de tratamientos "B":', r3)
    print('(r4) - Cantidad de tratamientos "C":', r4)
    print('(r5) - Cantidad de tratamientos "E":', r5)
    print('(r6) - Cantidad de tratamientos "P":', r6)
    print('(r7) – Importe final promedio (capítulo 19):', r7)
    print('(r8) – Paciente (no tipo "U") que pagó el mayor importe final:', r8)
    print('(r9) - Mayor importe pagado por ese paciente):', r9)
    print('(r10)- Porcentaje de tratamientos de alta complejidad con coste mayor al promedio:', r10)

principal()
