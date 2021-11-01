"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
import time
from DISClib.ADT import list as lt
from DISClib.DataStructures import orderedmapstructure as ord
from prettytable import PrettyTable
assert cf


def print_menu():
    """
    Imprime las opciones del menú.
    """
    print("\nBienvenido al menú.\n")
    print("0. Cargar datos y generar el catálogo.")
    print("1. Contar los avistamientos en una ciudad.")
    print("2. Contar los avistamientos por duración.")
    print("3. Contar avistamientos por hora/minutos del día.")
    print("4. Contar los avistamientos en un rango de fechas.")
    print("5. Contar los avistamientos de una zona geográfica.")
    print("6. Visualizar los avistamientos de una zona geográfica (Bono).")
    print("7. Detener la ejecución del programa.")


def print_load_data():
    print("Cargando información de los archivos...")
    start_time = time.process_time()
    catalog = init_catalog()
    load_data(catalog)
    controller.sort_sightings_req1(catalog)  # Requirement 1
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print('La carga de los datos demoró '+str(elapsed_time_mseg)+' ms.')
    return catalog


def init_catalog():
    """
    Inicializa el catalogo de libros.
    """
    return controller.init_catalog()


def load_data(catalog):
    """
    Carga los datos al catálogo.
    """
    return controller.load_data(catalog)


catalog = None


def print_req1(catalog):
    city = input('Ingrese el nombre de la ciudad a consultar: ')
    li = controller.requirement1(catalog, city)
    city = city.title()
    print('\n--------------------Requirement 1: Inputs--------------------\n')
    print('UFO sightings in the city of '+city+'.\n')
    print('\n--------------------Requirement 1: Answer--------------------\n')
    print('The city of '+city+' presents a total of '+str(lt.size(li)) +
          ' UFO sightings.')
    print("""Information regarding the first and last three UFO sightings in
             the city of """.replace('\n            ', '')+city +
          ' in chronological order:')
    table = PrettyTable(['Fecha y hora', 'Ciudad', 'País', 'Duración (s)',
                        'Forma'])
    for i in [1, 2, 3, -2, -1, 0]:
        table.add_row([lt.getElement(li, i)['datetime'],
                      lt.getElement(li, i)['city'],
                      lt.getElement(li, i)['country'],
                      lt.getElement(li, i)['duration (seconds)'],
                      lt.getElement(li, i)['shape']])
    print(table)


def print_req2():
    print('Este requerimiento aún no ha sido implementado.')


def print_req3():
    print('Este requerimiento aún no ha sido implementado.')


def print_req4():
    fechaMin = input("Digite la fecha minima: ")
    fechaMax = input("Digite la fecha maxima: ")
    print('Este requerimiento aún no ha sido implementado.')
    print(ord.minKey(catalog["req4"]))
    rango = controller.requirement4(catalog, fechaMin, fechaMax)
    print(rango)
    table = PrettyTable(['Fecha y hora', 'Ciudad', 'País', 'Duración (s)',
                        'Forma'])
    for i in [1, 2, 3, -2, -1, 0]:
        table.add_row([lt.getElement(rango, i)['datetime'],
                      lt.getElement(rango, i)['city'],
                      lt.getElement(rango, i)['country'],
                      lt.getElement(rango, i)['duration (seconds)'],
                      lt.getElement(rango, i)['shape']])
    print(table)


def print_req5():
    print('Este requerimiento aún no ha sido implementado.')


def print_req6():
    print('Este requerimiento aún no ha sido implementado.')


"""
Menú principal
"""
while True:
    error = '\nError: Por favor ingrese un número entero entre 0 y 7.\n'
    error_cargar = """\nError: Se deben cargar los datos antes de usar los
                      requisitos.\n""".replace('\n                     ', '')
    print_menu()
    try:
        inputs = int(input('Seleccione una opción para continuar: \n'))
    except Exception:
        print(error)
        continue
    if inputs == 0:
        catalog = print_load_data()
    elif inputs > 0 and inputs < 7:
        if type(catalog) != dict:
            print(error_cargar)
        elif inputs == 1:
            print_req1(catalog)
        elif inputs == 2:
            print_req2()
        elif inputs == 3:
            print_req3()
        elif inputs == 4:
            print_req4()
        elif inputs == 5:
            print_req5()
        elif inputs == 6:
            print_req6()
    elif inputs > 7:
        print(error)
    else:
        sys.exit(0)
sys.exit(0)
