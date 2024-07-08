""" 
Enunciado:
Se dispone de un archivo con datos acerca de los participantes de una carrera de bicicletas, que
tiene el siguiente formato:
id_bike, nombre (del dueño), tipo (bmx, playera, mtb, paseo), tiempo
por ejemplo: 50,jorge,bmx,0
51,sofia,paseo,0
52,andrea,mtb,0
Se deberá realizar un programa que permita el análisis de dicho archivo.
El programa contará con el siguiente menú:
1) Cargar archivo CSV: Se pedirá el nombre del archivo y se cargará en una lista de diccionarios
los elementos del mismo.
2) Imprimir lista: Se imprimirá por pantalla la tabla con los datos de las bicicletas.
3) Asignar tiempos: Se deberá mapear la lista con una función que asignará a cada bicicleta un
valor de tiempo entre 50 y 120 minutos calculado de manera aleatoria y se mostrará por pantalla la
lista.
4) Informar ganador: Informar el nombre del dueño de la bicicleta que llego primero y el tiempo
que tardo. Si hubiera empate. informar todos los nombres de las bicicletas que empataron.
5) Filtrar por tipo: Se deberá pedir un tipo de bicicleta al usuario y escribir un archivo igual al
original, pero donde solo aparezcan bicicletas del tipo seleccionado. El nombre del archivo será por
ejemplo playeras.csv
6) Informar promedio por tipo: Listar el promedio de tiempo por cada tipo de bicicleta.
7) Mostrar posiciones: Se deberá mostrar por pantalla un listado de las bicicletas ordenadas
por tipo y dentro de las del mismo tipo que aparezcan ordenadas por tiempo ascendente.
8) Guardar posiciones: Se deberá guardar el listado del punto anterior en un archivo JSON.
9) Salir.
"""
#Cargar archivo CSV: Se pedirá el nombre del archivo y se cargará en una lista de diccionarios
#los elementos del mismo.
def get_path_actual(nombre_archivo: str):
    """encuentra el archivo independientemente de en que path este

    Args:
        nombre_archivo (str): en este parametro se pone el nombre del archivo independientemente
                                de si esta el path o no

    Returns:
        _type_: retorna el nombre del archivo en su path actual 
    """
    import os
    directorio_actual = os.path.dirname(__file__)
    return os.path.join(directorio_actual, nombre_archivo)

def convertir_csv_lista_diccionarios(nombre_archivo: str)->list:
    """convierte un archivo csv en una lista de diccionarios

    Args:
        nombre_archivo (str): en este parametro se pone el nombre del archivo independientemente
                                de si esta el path o no

    Returns:
        list: la lista de diccionarios sacada del archivo csv
    """
    with open(get_path_actual(nombre_archivo), "r", encoding="utf-8") as archivo:
        lista = []
        encabezado = archivo.readline().strip("\n").split(",")
        # me trae las lineas que estan a continuacion
        for linea in archivo.readlines():
            persona = {}
            linea = linea.strip("\n").split(",")
            id_bike, nombre, tipo, tiempo = linea # esto es un desempaquetado de Lista
            
            persona["id_bike"] = int(id_bike)
            persona["nombre"] = nombre
            persona["tipo"] = tipo
            persona["tiempo"] = int(tiempo)
            lista.append(persona)
    return lista

# 2) Imprimir lista: Se imprimirá por pantalla la tabla con los datos de las bicicletas.
def imprimir_dato(diccionario: dict):
     print(f"{diccionario['id_bike']:<5} | {diccionario['nombre']:<30} | {diccionario['tipo']:<10} | {diccionario['tiempo']:>5}")

def imprimir_datos(lista: list):
    print("     ***Lista de bicis***")
    print(" ID        nombre                        tipo       tiempo")
    print("-------------------------------------------------------------")
    for e in lista: 
        imprimir_dato(e)

# 3) Asignar tiempos: Se deberá mapear la lista con una función que asignará a cada bicicleta un
# valor de tiempo entre 50 y 120 minutos calculado de manera aleatoria y se mostrará por pantalla la
# lista.
def asignar_tiempos(lista: list):
    """Asigna tiempos aleatorios entre 50 y 120 minutos a cada bicicleta"""
    import random
    for bici in lista:
        bici["tiempo"] = random.randint(50, 120)
    imprimir_datos(lista)

# 4) Informar ganador: Informar el nombre del dueño de la bicicleta que llego primero y el tiempo
# que tardo. Si hubiera empate. informar todos los nombres de las bicicletas que empataron.
def encontrar_extremo_manual(lista: list, clave: str, buscar_maximo: bool = True):
    """
    Encuentra el diccionario con el valor máximo o mínimo de una clave específica en una lista de diccionarios.

    Args:
        lista (list): Lista de diccionarios.
        clave (str): La clave por la cual buscar el valor extremo.
        buscar_maximo (bool): Indica si se busca el valor máximo (True) o mínimo (False). Por defecto es True.

    Returns:
        el valor extremo del diccionario que se pidio
    """
    if not lista:
        return None
    
    # Inicializar con el primer elemento de la lista
    extremo = lista[0][clave]
    
    # Iterar sobre la lista a partir del segundo elemento
    for item in lista[1:]:
        if buscar_maximo:
            if item[clave] > extremo:
                extremo = item[clave]
        else:
            if item[clave] < extremo:
                extremo = item[clave]
    
    return extremo

def informar_ganador(lista: list):
    """Informa el ganador o ganadores de la carrera"""
    if not lista:
        print("No hay datos cargados.")
        return
    
    min_tiempo = encontrar_extremo_manual(lista, "tiempo", buscar_maximo=False)
    ganadores = [bici for bici in lista if bici["tiempo"] == min_tiempo]
    
    print("Ganador/es:")
    
    for ganador in ganadores:
        print(f"Nombre: {ganador['nombre']}, Tiempo: {ganador['tiempo']}")

# 5) Filtrar por tipo: Se deberá pedir un tipo de bicicleta al usuario y escribir un archivo igual al
# original, pero donde solo aparezcan bicicletas del tipo seleccionado. El nombre del archivo será por
# ejemplo playeras.csv
def filtrar_lista(filtadora, lista: list):
    """Filtra una lista de elementos basándose en una función filtadora.

    Args:
        filtadora (_type_): es el criterio por el cual se va a filtrar
        lista (list): la lista que va a filtrar

    Returns:
        _type_: la lista filtrada
    """
    lista_filtrada = []
    for el in lista:
        if filtadora(el):
            lista_filtrada.append(el)
    return lista_filtrada

def filtro_tipo(diccionario, tipo: str):
    """Filtra una bicicleta por un tipo específico."""
    return diccionario['tipo'].upper() == tipo.upper()

def filtrar_por_tipo(lista: list, tipo_bici: str):
    """Filtra las bicicletas por tipo y guarda en un nuevo archivo CSV"""
    bicicletas_filtradas = filtrar_lista(lambda bici: filtro_tipo(bici, tipo_bici), lista)
    nombre_archivo = f"{tipo_bici.lower()}.csv"

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("id_bike,nombre,tipo,tiempo\n")
        for bici in bicicletas_filtradas:
            archivo.write(f"{bici['id_bike']},{bici['nombre']},{bici['tipo']},{bici['tiempo']}\n")

#6) Informar promedio por tipo: Listar el promedio de tiempo por cada tipo de bicicleta.
def informar_promedio_por_tipo(lista: list):
    """Informa el promedio de tiempo por cada tipo de bicicleta"""
    tipos = set(bici["tipo"] for bici in lista)
    
    for tipo in tipos:
        suma_tiempos = 0
        contador = 0
        
        for bici in lista:
            if bici["tipo"] == tipo:
                suma_tiempos += bici["tiempo"]
                contador += 1
        
        if contador > 0:
            promedio = suma_tiempos / contador
        else:
            promedio = 0
        
        print(f"Promedio de tiempo para {tipo}: {promedio:.2f} minutos")

# 7) Mostrar posiciones: Se deberá mostrar por pantalla un listado de las bicicletas ordenadas
# por tipo y dentro de las del mismo tipo que aparezcan ordenadas por tiempo ascendente.
def ordenar_bicicletas(lista: list, campo_1: str, campo_2: str) -> None:
    """Ordena la lista de bicicletas por un campo especificado."""
    n = len(lista)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if lista[i][campo_1] > lista[j][campo_1] or (lista[i][campo_1] == lista[j][campo_1] and lista[i][campo_2] > lista[j][campo_2]):
                lista[i], lista[j] = lista[j], lista[i]

def mostrar_posiciones(lista: list):
    """Muestra las bicicletas ordenadas por tipo y tiempo"""
    
    ordenar_bicicletas(lista, 'tipo', 'tiempo')
    imprimir_datos(lista)

# 8) Guardar posiciones: Se deberá guardar el listado del punto anterior en un archivo JSON.
def guardar_posiciones(lista: list):
    """Guarda las posiciones en un archivo JSON"""
    import json
    ordenar_bicicletas(lista, 'tipo', 'tiempo')
    nombre_archivo = "posiciones.json"
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(lista, archivo, ensure_ascii=False, indent=4)
    print(f"Archivo {nombre_archivo} creado con éxito.")

def main():
    lista_bicicletas = []
    opcion_1 = False
    opcion_3 = False
    bandera = True
    while bandera:
        print("\nMenú:")
        print("1) Cargar archivo CSV")
        print("2) Imprimir lista")
        print("3) Asignar tiempos")
        print("4) Informar ganador")
        print("5) Filtrar por tipo")
        print("6) Informar promedio por tipo")
        print("7) Mostrar posiciones")
        print("8) Guardar posiciones")
        print("9) Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre_archivo = "bicicletas.csv"
            lista_bicicletas = convertir_csv_lista_diccionarios(nombre_archivo)
            opcion_1 = True
        elif opcion == "2":
            if opcion_1:
                imprimir_datos(lista_bicicletas)
            else:
                print("NO ha cargado datos")
        elif opcion == "3":
            if opcion_1:
                asignar_tiempos(lista_bicicletas)
                opcion_3 = True
            else:
                print("NO ha cargado datos")
        elif opcion == "4":
            if opcion_1 and opcion_3:
                informar_ganador(lista_bicicletas)
            else:
                print("NO ha cargado datos o no ha asignado tiempos")
        elif opcion == "5":
            if opcion_1 and opcion_3:
                tipo_bici = input("Ingrese el tipo de bicicleta: ").upper()
                if tipo_bici == "PLAYERA" or tipo_bici == "BMX" or tipo_bici == "MTB" or tipo_bici == "PASEO":
                    filtrar_por_tipo(lista_bicicletas, tipo_bici)
                else:
                    print("Tipo no valido")
            else:
                print("NO ha cargado datos o no ha asignado tiempos")
        elif opcion == "6":
            if opcion_1 and opcion_3:
                informar_promedio_por_tipo(lista_bicicletas)
            else:
                print("NO ha cargado datos o no ha asignado tiempos")
        elif opcion == "7":
            if opcion_1 and opcion_3:
                mostrar_posiciones(lista_bicicletas)
            else:
                print("NO ha cargado datos o no ha asignado tiempos")
        elif opcion == "8":
            if opcion_1 and opcion_3:
                guardar_posiciones(lista_bicicletas)
            else:
                print("NO ha cargado datos o no ha asignado tiempos")
        elif opcion == "9":
            print("Saliendo del programa...")
            bandera = False
        else:
            print("Opción no válida, intente de nuevo.")


