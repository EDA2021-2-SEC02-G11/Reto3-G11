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
    catalog['cities'] = om.newMap(omaptype='RBT',
                                  comparefunction=compare_keys)
    return catalog


# Construccion de modelos

# Funciones para agregar informacion al catalogo


def add_sighting(catalog, sighting):
    # lt.addLast(catalog['crimes'], crime)
    update(catalog['cities'], sighting)
    return catalog


def update(map, sighting):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    city = sighting['city']
    date_time = datetime.datetime.strptime(sighting['datetime'],
                                           '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, city)
    if entry is None:
        dates = om.newMap(omaptype='RBT',
                          comparefunction=compare_keys)
        sightings_list = lt.newList('ARRAY_LIST')
        lt.addLast(sightings_list, sighting)
        om.put(dates, date_time, sightings_list)
        om.put(map, city, dates)
    else:
        dates = me.getValue(entry)
        sightings_entry = om.get(dates, date_time)
        if sightings_entry is None:
            sightings_list = lt.newList('ARRAY_LIST')
            lt.addLast(sightings_list, sighting)
            om.put(dates, date_time, sightings_list)
            om.put(map, city, dates)
        else:
            sightings_list = me.getValue(sightings_entry)
            lt.addLast(sightings_list, sighting)
            om.put(dates, date_time, sightings_list)
            om.put(map, city, dates)
    return map


# Requirements


def requirement1():
    pass


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
