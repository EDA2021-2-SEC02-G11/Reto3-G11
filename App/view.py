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
    print('\nBienvenido al menú.\n')
    print('0. Cargar datos y generar el catálogo.')
    print('1. Contar los avistamientos en una ciudad.')
    print('2. Contar los avistamientos por duración.')
    print('3. Contar avistamientos por hora/minutos del día.')
    print('4. Contar los avistamientos en un rango de fechas.')
    print('5. Contar los avistamientos de una zona geográfica.')
    print('6. Visualizar los avistamientos de una zona geográfica (Bono).')
    print('7. Detener la ejecución del programa.')


def print_load_data():
    print('Cargando información de los archivos...')
    start_time = time.process_time()
    catalog = init_catalog()
    load_data(catalog)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print('La carga de los datos demoró '+str(elapsed_time_mseg)+' ms.')
    print('Se cargaron '+str(lt.size(catalog['sightings']))+' avistamientos ' +
          'de OVNIS.')
    print('Primeros cinco y últimos cinco avistamientos cargados: ')
    table = PrettyTable(['Fecha y hora', 'Ciudad', 'País', 'Duración (s)',
                        'Forma'])
    ll = catalog['sightings']
    for i in [1, 2, 3, 4, 5, -4, -3, -2, -1, 0]:
        table.add_row([lt.getElement(ll, i)['datetime'],
                       lt.getElement(ll, i)['city'],
                       lt.getElement(ll, i)['country'],
                       lt.getElement(ll, i)['duration (seconds)'],
                       lt.getElement(ll, i)['shape']])
    print(table)
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
    total_cities, total, sample = controller.requirement1(catalog, city)
    city = city.title()
    print('\n--------------------Requirement 1: Inputs--------------------\n')
    print('UFO sightings in the city of '+city+'.\n')
    print('\n--------------------Requirement 1: Answer--------------------\n')
    print('The number of cities that present UFO sightings is ' +
          str(total_cities)+'.')
    print('The city of '+city+' presents a total of '+str(total) +
          ' UFO sightings.')
    print('Information regarding the first and last three UFO sightings in ' +
          'the city of '+city+' in chronological order:')
    table = PrettyTable(['Fecha y hora', 'Ciudad', 'País', 'Duración (s)',
                        'Forma'])
    for i in [1, 2, 3, 4, 5, 6]:
        table.add_row([lt.getElement(sample, i)['datetime'],
                      lt.getElement(sample, i)['city'],
                      lt.getElement(sample, i)['country'],
                      lt.getElement(sample, i)['duration (seconds)'],
                      lt.getElement(sample, i)['shape']])
    print(table)


def print_req2():
    sec_min = input('Ingrese un límite inferior en segundos: ')
    sec_max = input('Ingrese un límite superior en segundos: ')
    r2 = controller.requirement2(catalog, sec_min, sec_max)
    total_durations, top_duration, count_top = r2
    print('\n--------------------Requirement 2: Inputs--------------------\n')
    print('UFO sightings with durations bewteen '+str(float(sec_min))+' s ' +
          'and '+str(float(sec_max))+' s.\n')
    print('\n--------------------Requirement 2: Answer--------------------\n')
    print('There are '+str(total_durations)+' different durations of UFO ' +
          'sightings in total.')
    print('The longest UFO sighting recorded lasts for '+str(top_duration) +
          ' s. There are '+str(count_top)+' UFO sightings that last ' +
          'that long.')


def print_req3():
    print('Este requerimiento aún no ha sido implementado.')


def print_req4():
    fechaMin = input('Digite la fecha minima: ')
    fechaMax = input('Digite la fecha maxima: ')
    print('Este requerimiento aún no ha sido implementado.')
    print(ord.minKey(catalog['req4']))
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
    error_cargar = ('\nError: Se deben cargar los datos antes de usar los' +
                    ' requisitos.\n')
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
