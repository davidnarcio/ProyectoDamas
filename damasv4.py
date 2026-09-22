import os
import json

COLOR_BLANCA = "\033[97m"
COLOR_ROJA = "\033[91m"
COLOR_RESET = "\033[0m"

historial_movimientos = []

ARCHIVO_GUARDADO = "partida_guardada.json"


# Limpia 
def limpiar_pantalla():
    os.system("cls")


# Guarda un texto describiendo el movimiento que se acaba de hacer
def registrar_movimiento(jugador, nombre, f_ini, c_ini, f_fin, c_fin, es_captura):
    numero = len(historial_movimientos) + 1

    if jugador == "B":
        texto_jugador = "Blancas"
    else:
        texto_jugador = "Rojas"

    if es_captura:
        texto_accion = "captura y se mueve de"
    else:
        texto_accion = "se mueve de"

    origen = "(" + str(f_ini) + "," + str(c_ini) + ")"
    destino = "(" + str(f_fin) + "," + str(c_fin) + ")"

    texto = str(numero) + ". " + texto_jugador + ": " + nombre + " " + texto_accion + " " + origen + " a " + destino
    historial_movimientos.append(texto)


# Muestra los ultimos 15 movimientos
def mostrar_historial():
    print("\n--- Historial de movimientos ---")
    if len(historial_movimientos) == 0:
        print("(todavia no se ha movido ninguna ficha)")
        return

    movimientos_recientes = historial_movimientos[-15:]
    for texto in movimientos_recientes:
        print(texto)


tablero = []
nombres = []

for i in range(8):
    fila_tablero = []
    fila_nombres = []
    for j in range(8):
        fila_tablero.append(".")
        fila_nombres.append(".")
    tablero.append(fila_tablero)
    nombres.append(fila_nombres)


# Coloca una ficha en el tablero y guarda su nombre en la matriz de nombres
def colocar_pieza(fila, columna, tipo, nombre):
    tablero[fila][columna] = tipo
    nombres[fila][columna] = nombre


# Recorre todo el tablero buscando en que casilla esta esa ficha
def buscar_posicion_por_nombre(nombre_buscado):
    for i in range(8):
        for j in range(8):
            if nombres[i][j] == nombre_buscado:
                return i, j
    return None


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



def guardar_partida():
    datos = {
        "tablero": tablero,
        "nombres": nombres,
        "turno": turno,
        "historial_movimientos": historial_movimientos
    }
    with open(ARCHIVO_GUARDADO, "w") as archivo:
        json.dump(datos, archivo)
    print("Partida guardada en '" + ARCHIVO_GUARDADO + "'.")


def existe_partida_guardada():
    return os.path.exists(ARCHIVO_GUARDADO)


def cargar_partida():
    global tablero, nombres, turno, historial_movimientos

    with open(ARCHIVO_GUARDADO, "r") as archivo:
        datos = json.load(archivo)

    tablero = datos["tablero"]
    nombres = datos["nombres"]
    turno = datos["turno"]
    historial_movimientos = datos["historial_movimientos"]


# Borra el archivo de partida guardada (se usa cuando el juego termina normalmente)
def borrar_partida_guardada():
    if existe_partida_guardada():
        os.remove(ARCHIVO_GUARDADO)


# Si hay una partida guardada, pregunta al usuario si quiere continuarla
def preguntar_si_cargar_partida():
    if not existe_partida_guardada():
        return

    while True:
        respuesta = input("Se encontro una partida guardada. Deseas cargarla? (s/n): ")
        respuesta = respuesta.strip().lower()

        if respuesta == "s":
            cargar_partida()
            print("Partida cargada.")
            return

        if respuesta == "n":
            borrar_partida_guardada()
            return

        print("Respuesta invalida. Escribe 's' o 'n'.")


# Imprime el tablero completo, con colores y nombres de fichas
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
                nombre = nombres[i][j]
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


# Dice si la pieza es del jugador indicado ("B" o "R")
def es_pieza_del_jugador(pieza, jugador):
    if jugador == "B":
        return pieza == "b" or pieza == "B"
    else:
        return pieza == "r" or pieza == "R"


# Dice si la pieza es del rival (y no esta vacia)
def es_pieza_del_rival(pieza, jugador):
    if pieza == ".":
        return False
    return not es_pieza_del_jugador(pieza, jugador)


# Una ficha es dama si su letra esta en mayuscula
def es_dama(pieza):
    return pieza == "B" or pieza == "R"


# Si una ficha llega al extremo opuesto del tablero, se vuelve dama
def convertir_en_dama_si_corresponde(fila, columna):
    pieza = tablero[fila][columna]
    if pieza == "b" and fila == 7:
        tablero[fila][columna] = "B"
    if pieza == "r" and fila == 0:
        tablero[fila][columna] = "R"


# Revisa si un movimiento (simple o captura) es valido.
# es_captura=False -> se mueve 1 casilla, es_captura=True -> se mueve 2 (y come)
def movimiento_valido(f_ini, c_ini, f_fin, c_fin, jugador, es_captura):
    if f_fin < 0 or f_fin > 7 or c_fin < 0 or c_fin > 7:
        return False

    if tablero[f_fin][c_fin] != ".":
        return False

    diferencia_fila = f_fin - f_ini
    diferencia_columna = c_fin - c_ini

    if es_captura:
        distancia = 2
    else:
        distancia = 1

    if abs(diferencia_fila) != distancia or abs(diferencia_columna) != distancia:
        return False

    if es_captura:
        f_medio = (f_ini + f_fin) // 2
        c_medio = (c_ini + c_fin) // 2
        pieza_medio = tablero[f_medio][c_medio]
        if not es_pieza_del_rival(pieza_medio, jugador):
            return False

    pieza = tablero[f_ini][c_ini]

    if es_dama(pieza):
        return True

    if jugador == "B":
        return diferencia_fila == distancia
    else:
        return diferencia_fila == -distancia


# Mueve una ficha de una casilla a otra, actualizando el tablero y la
# matriz de nombres. Si es_captura=True, primero borra la ficha del medio.
def mover_ficha(f_ini, c_ini, f_fin, c_fin, es_captura):
    if es_captura:
        f_medio = (f_ini + f_fin) // 2
        c_medio = (c_ini + c_fin) // 2
        tablero[f_medio][c_medio] = "."
        nombres[f_medio][c_medio] = "."

    nombre = nombres[f_ini][c_ini]
    tablero[f_fin][c_fin] = tablero[f_ini][c_ini]
    tablero[f_ini][c_ini] = "."

    nombres[f_fin][c_fin] = nombre
    nombres[f_ini][c_ini] = "."


# Revisa si desde esta casilla hay alguna captura posible
def existe_captura_desde(fila, columna, jugador):
    direcciones = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
    for direccion in direcciones:
        f_fin = fila + direccion[0]
        c_fin = columna + direccion[1]
        if movimiento_valido(fila, columna, f_fin, c_fin, jugador, True):
            return True
    return False


# Revisa todo el tablero buscando si el jugador tiene alguna captura obligatoria
def jugador_tiene_captura_obligatoria(jugador):
    for i in range(8):
        for j in range(8):
            pieza = tablero[i][j]
            if es_pieza_del_jugador(pieza, jugador):
                if existe_captura_desde(i, j, jugador):
                    return True
    return False


# Revisa si el jugador tiene algun movimiento posible (para saber si perdio)
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
                    if movimiento_valido(i, j, f_fin, c_fin, jugador, False):
                        return True

    return False


def contar_fichas(jugador):
    contador = 0
    for i in range(8):
        for j in range(8):
            if es_pieza_del_jugador(tablero[i][j], jugador):
                contador = contador + 1
    return contador


# Dice si moverse en esa direccion es ir "adelante" o "atras" para el jugador
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


# Junta todos los movimientos posibles de una ficha en una sola lista.
# es_captura decide si busca movimientos simples o capturas.
def obtener_opciones(fila, columna, jugador, es_captura):
    opciones = []

    if es_captura:
        posibles_direcciones = [(2, -2), (2, 2), (-2, -2), (-2, 2)]
    else:
        posibles_direcciones = [(1, -1), (1, 1), (-1, -1), (-1, 1)]

    for direccion in posibles_direcciones:
        diferencia_fila = direccion[0]
        diferencia_columna = direccion[1]
        f_fin = fila + diferencia_fila
        c_fin = columna + diferencia_columna

        if movimiento_valido(fila, columna, f_fin, c_fin, jugador, es_captura):
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


# Si hay una sola opcion, se mueve sola. Si hay varias, pregunta al usuario
# (primero adelante/atras si hace falta, despues izquierda/derecha).
def elegir_movimiento(opciones):
    if len(opciones) == 1:
        anunciar_movimiento_automatico(opciones[0])
        return opciones[0]

    hay_adelante = False
    hay_atras = False
    for opcion in opciones:
        if opcion["sentido"] == "adelante":
            hay_adelante = True
        else:
            hay_atras = True

    if hay_adelante and hay_atras:
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


# Pide el nombre de una ficha hasta que el usuario escriba una valida y suya.
# Si el usuario escribe "salir", devuelve None para indicar que quiere salir.
def leer_nombre_ficha(mensaje, jugador):
    while True:
        texto = input(mensaje)
        texto = texto.strip().lower()

        if texto == "salir":
            return None

        posicion = buscar_posicion_por_nombre(texto)
        if posicion is None:
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

preguntar_si_cargar_partida()

juego_activo = True

while juego_activo:

    limpiar_pantalla()
    mostrar_tablero()
    mostrar_historial()

    fichas_blancas = contar_fichas("B")
    fichas_rojas = contar_fichas("R")

    if fichas_blancas == 0:
        print("Las rojas ganan, las blancas ya no tienen fichas.")
        borrar_partida_guardada()
        juego_activo = False
        break

    if fichas_rojas == 0:
        print("Las blancas ganan, las rojas ya no tienen fichas.")
        borrar_partida_guardada()
        juego_activo = False
        break

    if not jugador_tiene_movimiento_disponible(turno):
        if turno == "B":
            print("Las blancas no tienen movimientos disponibles. Ganan las rojas.")
        else:
            print("Las rojas no tienen movimientos disponibles. Ganan las blancas.")
        borrar_partida_guardada()
        juego_activo = False
        break

    if turno == "B":
        print("Turno de las BLANCAS")
    else:
        print("Turno de las ROJAS")

    hay_captura_obligatoria = jugador_tiene_captura_obligatoria(turno)
    if hay_captura_obligatoria:
        print("Tienes una captura disponible, es obligatorio realizarla.")

    nombre_ficha = leer_nombre_ficha(
        "Escribe el nombre de la ficha que quieres mover (ejemplo: b3), o escribe 'salir' para guardar y salir: ",
        turno
    )

    if nombre_ficha is None:
        guardar_partida()
        print("Hasta luego! La proxima vez que inicies el juego podras continuar esta partida.")
        juego_activo = False
        break

    fila, columna = buscar_posicion_por_nombre(nombre_ficha)

    opciones = obtener_opciones(fila, columna, turno, hay_captura_obligatoria)

    if len(opciones) == 0:
        if hay_captura_obligatoria:
            print("Esa ficha no tiene captura disponible. Elige otra ficha.")
        else:
            print("Esa ficha no tiene movimientos disponibles. Elige otra ficha.")
        continue

    movimiento = elegir_movimiento(opciones)

    mover_ficha(fila, columna, movimiento["fila_fin"], movimiento["columna_fin"], hay_captura_obligatoria)
    convertir_en_dama_si_corresponde(movimiento["fila_fin"], movimiento["columna_fin"])
    registrar_movimiento(turno, nombre_ficha, fila, columna, movimiento["fila_fin"], movimiento["columna_fin"], hay_captura_obligatoria)

    if hay_captura_obligatoria:
        f_actual = movimiento["fila_fin"]
        c_actual = movimiento["columna_fin"]

        while existe_captura_desde(f_actual, c_actual, turno):
            limpiar_pantalla()
            mostrar_tablero()
            mostrar_historial()
            print("Puedes seguir comiendo con la misma ficha.")

            opciones_extra = obtener_opciones(f_actual, c_actual, turno, True)
            movimiento_extra = elegir_movimiento(opciones_extra)

            mover_ficha(f_actual, c_actual, movimiento_extra["fila_fin"], movimiento_extra["columna_fin"], True)
            convertir_en_dama_si_corresponde(movimiento_extra["fila_fin"], movimiento_extra["columna_fin"])
            registrar_movimiento(turno, nombre_ficha, f_actual, c_actual, movimiento_extra["fila_fin"], movimiento_extra["columna_fin"], True)

            f_actual = movimiento_extra["fila_fin"]
            c_actual = movimiento_extra["columna_fin"]

    if turno == "B":
        turno = "R"
    else:
        turno = "B"