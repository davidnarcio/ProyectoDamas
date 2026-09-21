COLOR_BLANCA = "\033[97m"   
COLOR_ROJA = "\033[91m"     
COLOR_RESET = "\033[0m"

tablero = []

for i in range(8):
    fila = []
    for j in range(8):
        fila.append(".")
    tablero.append(fila)


nombre_a_posicion = {}
posicion_a_nombre = {}


def colocar_pieza(fila, columna, tipo, nombre):
    tablero[fila][columna] = tipo
    nombre_a_posicion[nombre] = (fila, columna)
    posicion_a_nombre[(fila, columna)] = nombre


contador_b = 1
for i in range(0, 3):
    for j in range(8):
        if (i + j) % 2 == 1:
            nombre = "b" + str(contador_b)
            colocar_pieza(i, j, "b", nombre)
            contador_b = contador_b + 1

contador_r = 1
for i in range(5, 8):
    for j in range(8):
        if (i + j) % 2 == 1:
            nombre = "r" + str(contador_r)
            colocar_pieza(i, j, "r", nombre)
            contador_r = contador_r + 1

turno = "B"


def mostrar_tablero():
    print(" ")
    encabezado = "    "
    for j in range(8):
        encabezado = encabezado + str(j).ljust(6)
    print(encabezado)

    for i in range(8):
        linea = str(i).ljust(4)
        for j in range(8):
            pieza = tablero[i][j]
            if pieza == ".":
                linea = linea + ".".ljust(6)
            else:
                nombre = posicion_a_nombre[(i, j)]
                if pieza == "b" or pieza == "B":
                    color = COLOR_BLANCA
                else:
                    color = COLOR_ROJA
                if pieza == "B" or pieza == "R":
                    texto_nombre = nombre.upper()
                else:
                    texto_nombre = nombre
                celda = color + texto_nombre + COLOR_RESET
                espacios = 6 - len(texto_nombre)
                linea = linea + celda + " " * espacios
        print(linea)


def es_pieza_del_jugador(pieza, jugador):
    if jugador == "B":
        if pieza == "b" or pieza == "B":
            return True
        else:
            return False
    else:
        if pieza == "r" or pieza == "R":
            return True
        else:
            return False


def es_pieza_del_rival(pieza, jugador):
    if pieza == ".":
        return False
    if es_pieza_del_jugador(pieza, jugador):
        return False
    return True


def es_dama(pieza):
    if pieza == "B" or pieza == "R":
        return True
    else:
        return False


def convertir_en_dama_si_corresponde(fila, columna):
    pieza = tablero[fila][columna]
    if pieza == "b" and fila == 7:
        tablero[fila][columna] = "B"
    if pieza == "r" and fila == 0:
        tablero[fila][columna] = "R"


def movimiento_simple_es_valido(f_ini, c_ini, f_fin, c_fin, jugador):
    if f_fin < 0 or f_fin > 7 or c_fin < 0 or c_fin > 7:
        return False

    if tablero[f_fin][c_fin] != ".":
        return False

    diferencia_fila = f_fin - f_ini
    diferencia_columna = c_fin - c_ini

    if abs(diferencia_fila) != 1 or abs(diferencia_columna) != 1:
        return False

    pieza = tablero[f_ini][c_ini]

    if es_dama(pieza):
        return True

    if jugador == "B":
        if diferencia_fila == 1:
            return True
        else:
            return False
    else:
        if diferencia_fila == -1:
            return True
        else:
            return False


def captura_es_valida(f_ini, c_ini, f_fin, c_fin, jugador):
    if f_fin < 0 or f_fin > 7 or c_fin < 0 or c_fin > 7:
        return False

    if tablero[f_fin][c_fin] != ".":
        return False

    diferencia_fila = f_fin - f_ini
    diferencia_columna = c_fin - c_ini

    if abs(diferencia_fila) != 2 or abs(diferencia_columna) != 2:
        return False

    f_medio = (f_ini + f_fin) // 2
    c_medio = (c_ini + c_fin) // 2
    pieza_de_en_medio = tablero[f_medio][c_medio]

    if not es_pieza_del_rival(pieza_de_en_medio, jugador):
        return False

    pieza = tablero[f_ini][c_ini]

    if es_dama(pieza):
        return True

    if jugador == "B":
        if diferencia_fila == 2:
            return True
        else:
            return False
    else:
        if diferencia_fila == -2:
            return True
        else:
            return False


def mover_ficha_simple(f_ini, c_ini, f_fin, c_fin):
    nombre = posicion_a_nombre[(f_ini, c_ini)]

    tablero[f_fin][c_fin] = tablero[f_ini][c_ini]
    tablero[f_ini][c_ini] = "."

    del posicion_a_nombre[(f_ini, c_ini)]
    posicion_a_nombre[(f_fin, c_fin)] = nombre
    nombre_a_posicion[nombre] = (f_fin, c_fin)


def hacer_captura(f_ini, c_ini, f_fin, c_fin):
    f_medio = (f_ini + f_fin) // 2
    c_medio = (c_ini + c_fin) // 2

    nombre_comida = posicion_a_nombre[(f_medio, c_medio)]
    tablero[f_medio][c_medio] = "."
    del nombre_a_posicion[nombre_comida]
    del posicion_a_nombre[(f_medio, c_medio)]

    mover_ficha_simple(f_ini, c_ini, f_fin, c_fin)


def existe_captura_desde(fila, columna, jugador):
    direcciones = [(2, 2), (2, -2), (-2, 2), (-2, -2)]

    for direccion in direcciones:
        f_fin = fila + direccion[0]
        c_fin = columna + direccion[1]
        if captura_es_valida(fila, columna, f_fin, c_fin, jugador):
            return True

    return False


def jugador_tiene_captura_obligatoria(jugador):
    for i in range(8):
        for j in range(8):
            pieza = tablero[i][j]
            if es_pieza_del_jugador(pieza, jugador):
                if existe_captura_desde(i, j, jugador):
                    return True
    return False


def jugador_tiene_movimiento_disponible(jugador):
    if jugador_tiene_captura_obligatoria(jugador):
        return True

    direcciones = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for i in range(8):
        for j in range(8):
            pieza = tablero[i][j]
            if es_pieza_del_jugador(pieza, jugador):
                for direccion in direcciones:
                    f_fin = i + direccion[0]
                    c_fin = j + direccion[1]
                    if movimiento_simple_es_valido(i, j, f_fin, c_fin, jugador):
                        return True

    return False


def contar_fichas(jugador):
    contador = 0
    for i in range(8):
        for j in range(8):
            if es_pieza_del_jugador(tablero[i][j], jugador):
                contador = contador + 1
    return contador


def calcular_sentido(diferencia_fila, jugador):
    if jugador == "B":
        if diferencia_fila > 0:
            return "adelante"
        else:
            return "atras"
    else:
        if diferencia_fila < 0:
            return "adelante"
        else:
            return "atras"


def obtener_opciones_movimiento_simple(fila, columna, jugador):
    opciones = []
    posibles_direcciones = [(1, -1), (1, 1), (-1, -1), (-1, 1)]

    for direccion in posibles_direcciones:
        diferencia_fila = direccion[0]
        diferencia_columna = direccion[1]
        f_fin = fila + diferencia_fila
        c_fin = columna + diferencia_columna

        if movimiento_simple_es_valido(fila, columna, f_fin, c_fin, jugador):
            if diferencia_columna == -1:
                lado = "i"
            else:
                lado = "d"
            sentido = calcular_sentido(diferencia_fila, jugador)
            opciones.append({"fila_fin": f_fin, "columna_fin": c_fin, "lado": lado, "sentido": sentido})

    return opciones


def obtener_opciones_captura(fila, columna, jugador):
    opciones = []
    posibles_direcciones = [(2, -2), (2, 2), (-2, -2), (-2, 2)]

    for direccion in posibles_direcciones:
        diferencia_fila = direccion[0]
        diferencia_columna = direccion[1]
        f_fin = fila + diferencia_fila
        c_fin = columna + diferencia_columna

        if captura_es_valida(fila, columna, f_fin, c_fin, jugador):
            if diferencia_columna < 0:
                lado = "i"
            else:
                lado = "d"
            sentido = calcular_sentido(diferencia_fila, jugador)
            opciones.append({"fila_fin": f_fin, "columna_fin": c_fin, "lado": lado, "sentido": sentido})

    return opciones


def anunciar_movimiento_automatico(opcion):
    if opcion["lado"] == "d":
        print("Esa ficha solo puede moverse hacia la derecha, se movera automaticamente.")
    else:
        print("Esa ficha solo puede moverse hacia la izquierda, se movera automaticamente.")


def elegir_movimiento(opciones):
    # Si solo hay una opcion en total, no hay nada que preguntar.
    if len(opciones) == 1:
        anunciar_movimiento_automatico(opciones[0])
        return opciones[0]

    # Si la ficha es una dama y puede moverse tanto hacia adelante como
    # hacia atras, primero se pregunta el sentido.
    sentidos_disponibles = set()
    for opcion in opciones:
        sentidos_disponibles.add(opcion["sentido"])

    if len(sentidos_disponibles) > 1:
        while True:
            respuesta = input("Quieres mover la dama hacia adelante o hacia atras? Escribe 'w' (adelante) o 's' (atras): ")
            respuesta = respuesta.strip().lower()

            if respuesta != "w" and respuesta != "s":
                print("Respuesta invalida. Escribe 'w' o 's'.")
                continue

            if respuesta == "w":
                sentido_elegido = "adelante"
            else:
                sentido_elegido = "atras"

            filtradas = []
            for opcion in opciones:
                if opcion["sentido"] == sentido_elegido:
                    filtradas.append(opcion)

            if len(filtradas) == 0:
                print("No hay movimiento disponible en ese sentido. Intenta de nuevo.")
                continue

            opciones = filtradas
            break

    # Una vez resuelto el sentido (o si no hacia falta), si solo queda
    # una opcion se mueve sola; si quedan dos, se pregunta el lado.
    if len(opciones) == 1:
        anunciar_movimiento_automatico(opciones[0])
        return opciones[0]

    while True:
        respuesta = input("Hacia donde quieres mover la ficha? Escribe 'd' (derecha) o 'a' (izquierda): ")
        respuesta = respuesta.strip().lower()

        if respuesta != "d" and respuesta != "a":
            print("Respuesta invalida. Escribe 'd' o 'a'.")
            continue

        if respuesta == "a":
            lado_elegido = "i"
        else:
            lado_elegido = "d"

        filtradas = []
        for opcion in opciones:
            if opcion["lado"] == lado_elegido:
                filtradas.append(opcion)

        if len(filtradas) == 0:
            print("No hay movimiento disponible hacia ese lado. Intenta de nuevo.")
            continue

        return filtradas[0]


def leer_nombre_ficha(mensaje, jugador):
    while True:
        texto = input(mensaje)
        texto = texto.strip().lower()

        if texto not in nombre_a_posicion:
            print("Esa ficha no existe. Intenta de nuevo.")
            continue

        if jugador == "B" and texto[0] != "b":
            print("Esa ficha no es tuya. Intenta de nuevo.")
            continue

        if jugador == "R" and texto[0] != "r":
            print("Esa ficha no es tuya. Intenta de nuevo.")
            continue

        return texto


# MAIN

juego_activo = True

while juego_activo:

    mostrar_tablero()

    fichas_blancas = contar_fichas("B")
    fichas_rojas = contar_fichas("R")

    if fichas_blancas == 0:
        print("Las rojas ganan, las blancas ya no tienen fichas.")
        juego_activo = False
        break

    if fichas_rojas == 0:
        print("Las blancas ganan, las rojas ya no tienen fichas.")
        juego_activo = False
        break

    if not jugador_tiene_movimiento_disponible(turno):
        if turno == "B":
            print("Las blancas no tienen movimientos disponibles. Ganan las rojas.")
        else:
            print("Las rojas no tienen movimientos disponibles. Ganan las blancas.")
        juego_activo = False
        break

    if turno == "B":
        print("Turno de las BLANCAS")
    else:
        print("Turno de las ROJAS")

    hay_captura_obligatoria = jugador_tiene_captura_obligatoria(turno)
    if hay_captura_obligatoria:
        print("Tienes una captura disponible, es obligatorio realizarla.")

    nombre_ficha = leer_nombre_ficha("Escribe el nombre de la ficha que quieres mover (ejemplo: b3): ", turno)
    fila, columna = nombre_a_posicion[nombre_ficha]

    if hay_captura_obligatoria:
        opciones = obtener_opciones_captura(fila, columna, turno)
        es_captura = True
    else:
        opciones = obtener_opciones_movimiento_simple(fila, columna, turno)
        es_captura = False

    if len(opciones) == 0:
        if es_captura:
            print("Esa ficha no tiene captura disponible. Elige otra ficha.")
        else:
            print("Esa ficha no tiene movimientos disponibles. Elige otra ficha.")
        continue

    movimiento = elegir_movimiento(opciones)

    if es_captura:
        hacer_captura(fila, columna, movimiento["fila_fin"], movimiento["columna_fin"])
        convertir_en_dama_si_corresponde(movimiento["fila_fin"], movimiento["columna_fin"])

        f_actual = movimiento["fila_fin"]
        c_actual = movimiento["columna_fin"]

        while existe_captura_desde(f_actual, c_actual, turno):
            mostrar_tablero()
            print("Puedes seguir comiendo con la misma ficha.")
            opciones_extra = obtener_opciones_captura(f_actual, c_actual, turno)
            movimiento_extra = elegir_movimiento(opciones_extra)

            hacer_captura(f_actual, c_actual, movimiento_extra["fila_fin"], movimiento_extra["columna_fin"])
            convertir_en_dama_si_corresponde(movimiento_extra["fila_fin"], movimiento_extra["columna_fin"])

            f_actual = movimiento_extra["fila_fin"]
            c_actual = movimiento_extra["columna_fin"]
    else:
        mover_ficha_simple(fila, columna, movimiento["fila_fin"], movimiento["columna_fin"])
        convertir_en_dama_si_corresponde(movimiento["fila_fin"], movimiento["columna_fin"])

    if turno == "B":
        turno = "R"
    else:
        turno = "B"