"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from datetime import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import mergesort as mer
from DISClib.DataStructures import mapentry as me
assert cf


def new_catalog():
    """
    Crea el catálogo.
    """
    catalog = {}

    catalog['req1'] = om.newMap(omaptype='RBT',
                                comparefunction=compare_keys)
    catalog['req4'] = om.newMap(omaptype='RBT',
                                comparefunction=compare_datetime)

    return catalog


# Construccion de modelos

# Funciones para agregar informacion al catalogo


def add_sighting(catalog, sighting):
    create_tree_req1(catalog['req1'], sighting)  # Requirement 1
    create_tree_req4(catalog['req4'], sighting)  # Requirement 4
    return catalog


# Lab 8


def opcion3(catalog):
    height = om.height(catalog['req1'])
    size = om.size(catalog['req1'])
    return height, size


# Requirement 1


def create_tree_req1(tree, sighting):
    """
    Crea el árbol del requisito 1.
    El árbol tiene como llaves ciudades y como valores arreglos con los
    avistamientos en por ciudad.
    """
    city = sighting['city']
    entry = om.get(tree, city)
    if entry is None:
        sightings_list = lt.newList('ARRAY_LIST')
    else:
        sightings_list = me.getValue(entry)
    lt.addLast(sightings_list, sighting)
    om.put(tree, city, sightings_list)
    return tree


def sort_sightings_req1(catalog):
    tree = catalog['req1']
    keys = om.keySet(tree)
    for city in lt.iterator(keys):
        entry = om.get(tree, city)
        sightings_list = me.getValue(entry)
        sorted_sightings = mer.sort(sightings_list, compare_datetime)
        om.put(tree, city, sorted_sightings)
    entry = om.get(tree, 'las vegas')
    return tree


def requirement1(catalog, city):
    """
    Arma la respuesta del requisito 1 usando el árbol del requisito 1.
    """
    entry = om.get(catalog['req1'], city)
    sightings_list = me.getValue(entry)
    return sightings_list


def requirement2():
    pass


def requirement3():
    pass

# Requirement 4

def create_tree_req4(tree, sighting):
    """
    Crea el árbol del requisito 4.
    El árbol tiene como llaves las fechas de avistamientos y como valores arreglos con los
    avistamientos por fecha.
    """
    time=sighting["datetime"]
    entry= om.get(tree, time)
    if entry is None:
        sightings_list = lt.newList('ARRAY_LIST')
    else:
        sightings_list = me.getValue(entry)
    lt.addLast(sightings_list, sighting)
    om.put(tree, time, sightings_list)
    return tree


def requirement4(catalog):
    pass


def requirement5():
    pass


def requirement6():
    pass


# Compare functions


def compare_keys(key1, key2):
    """
    Compara dos elementos cualquiera.
    """
    if key1 == key2:
        return 0
    elif key1 > key2:
        return 1
    else:
        return -1


def compare_datetime(sighting1, sighting2):
    """
    Compara dos fechas con hora en el formato YYYY-MM-DD HH:MM:SS
    usando la libreria Datetime.
    """
    print(sighting1)
    datetime1 = datetime.strptime(sighting1,
                                           '%Y-%m-%d %H:%M:%S')
    datetime2 = datetime.strptime(sighting2,
                                           '%Y-%m-%d %H:%M:%S')
    if datetime1 == datetime2:
        return 0
    elif datetime1 > datetime2:
        return 1
    else:
        return -1


# Funciones de ordenamiento
