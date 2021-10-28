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
import datetime
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
assert cf


def new_catalog():
    """
    Crea el catálogo.
    """
    catalog = {}

    catalog['req1'] = om.newMap(omaptype='RBT',
                                comparefunction=compare_keys)

    return catalog


# Construccion de modelos

# Funciones para agregar informacion al catalogo


def add_sighting(catalog, sighting):
    create_tree_req1(catalog['req1'], sighting)  # Requirement 1
    return catalog


# Lab 8


def opcion3(catalog):
    height = om.height(catalog['req1'])
    size = om.size(catalog['req1'])
    return height, size


# Requirement 1


def create_tree_req1(map, sighting):
    """
    Crea el árbol del requisito 1.
    El árbol que tiene como llaves ciudades y como valores diccionarios.
    En el diccionario hay dos parejas llave valor: una para el total de
    avistamientos en la ciudad y otra que es un árbol. El árbol tiene como
    llaves fechas (con hora) y como valores arreglos. Cada arreglo contiene los
    avistamientos en una fecha y ciudad determinadas.
    """
    city = sighting['city']
    date_time = datetime.datetime.strptime(sighting['datetime'],
                                           '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, city)
    if entry is None:
        structure = {'total': 0, 'dates': om.newMap(omaptype='RBT',
                     comparefunction=compare_keys)}
        sightings_list = lt.newList('ARRAY_LIST', key='city')
        lt.addLast(sightings_list, sighting)
        structure['total'] += 1
        om.put(structure['dates'], date_time, sightings_list)
        om.put(map, city, structure)
    else:
        structure = me.getValue(entry)
        sightings_entry = om.get(structure['dates'], date_time)
        if sightings_entry is None:
            sightings_list = lt.newList('ARRAY_LIST')
            lt.addLast(sightings_list, sighting)
            structure['total'] += 1
            om.put(structure['dates'], date_time, sightings_list)
            om.put(map, city, structure)
        else:
            sightings_list = me.getValue(sightings_entry)
            lt.addLast(sightings_list, sighting)
            structure['total'] += 1
            om.put(structure['dates'], date_time, sightings_list)
            om.put(map, city, structure)
    return map


def requirement1(catalog, city):
    """
    Arma la respuesta del requisito 1 usando el árbol del requisito 1.
    """
    sample = lt.newList('ARRAY_LIST')
    entry = om.get(catalog['req1'], city)
    structure = me.getValue(entry)
    total = structure['total']
    dates = structure['dates']

    return total, sample 


def requirement2():
    pass


def requirement3():
    pass


def requirement4():
    pass


def requirement5():
    pass


def requirement6():
    pass


# Compare functions


def compare_keys(key1, key2):
    """
    Compara dos ciudades.
    """
    if key1 == key2:
        return 0
    elif key1 > key2:
        return 1
    else:
        return -1

# Funciones de ordenamiento
