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
assert cf


def print_menu():
    """
    Imprime las opciones del menú.
    """
    print("\nBienvenido al menú.\n")
    print("0. Cargar datos y generar el catálogo.")
    print("Req. 1. Contar los avistamientos en una ciudad.")
    print("Req. 2. Contar los avistamientos por duración.")
    print("Req. 3. Contar avistamientos por hora/minutos del día.")
    print("Req. 4. Contar los avistamientos en un rango de fechas.")
    print("Req. 5. Contar los avistamientos de una zona geográfica.")
    print("Req. 6 (B). Visualizar los avistamientos de una zona geográfica.")
    print("7. Detener la ejecución del programa.")


def print_load_data():
    print("Cargando información de los archivos...")
    start_time = time.process_time()
    catalog = init_catalog()
    load_data(catalog)
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


def print_req_1():
    print('Este requerimiento aún no ha sido implementado.')


def print_req_2():
    print('Este requerimiento aún no ha sido implementado.')


def print_req_3():
    print('Este requerimiento aún no ha sido implementado.')


def print_req_4():
    print('Este requerimiento aún no ha sido implementado.')


def print_req_5():
    print('Este requerimiento aún no ha sido implementado.')


def print_req_6():
    print('Este requerimiento aún no ha sido implementado.')


"""
Menú principal
"""
while True:
    error = '\nError: Por favor ingrese un número entero entre 0 y 7.\n'
    error_cargar = """\nError: Se deben cargar los datos antes de usar los
                      requisitos.\n""".replace('\n                      ', ' ')
    print_menu()
    try:
        inputs = int(input('Seleccione una opción para continuar: \n'))
    except:
        print(error)
        continue
    if inputs == 0:
        catalog = load_data()
    elif inputs > 0 and inputs < 7:
        if type(catalog) != dict:
            print(error_cargar)
        elif inputs == 1:
            print_req_1()
        elif inputs == 2:
            print_req_2()
        elif inputs == 3:
            print_req_3()
        elif inputs == 4:
            print_req_4()
        elif inputs == 5:
            print_req_5()
        elif inputs == 6:
            print_req_6()
    elif inputs > 7:
        print(error)
    else:
        sys.exit(0)
sys.exit(0)
