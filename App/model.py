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
                                comparefunction=compareTime)

    return catalog


# Construccion de modelos

# Funciones para agregar informacion al catalogo


def add_sighting(catalog, sighting):
    create_tree_req1(catalog['req1'], sighting)  # Requirement 1
    create_tree_req4(catalog['req4'], sighting)  # Requirement 4
    return catalog


# Requirement 1


def create_tree_req1(map, sighting):
    """
    Crea el árbol del requisito 1.
    El árbol tiene como llaves ciudades y como valores árboles.
    Cada árbol tiene como llaves fechas (con hora, en formato datetime) y el
    valor correspondiente a cada llave es el avistamiento en la ciudad dada a
    la fecha y hora de la llave.
    Nótese que en los datos no hay dos avistamientos que hayan ocurrido en la
    misma ciudad y en la misma fecha, hora, minuto y segundo.
    """
    entry = om.get(map, sighting['city'])
    if entry is None:
        dates = om.newMap(omaptype='RBT',
                          comparefunction=compare_keys)
        date = datetime.strptime(sighting['datetime'],
                                 '%Y-%m-%d %H:%M:%S')
        om.put(dates, date, sighting)
        om.put(map, sighting['city'], dates)
    else:
        dates = me.getValue(entry)
        date = datetime.strptime(sighting['datetime'],
                                 '%Y-%m-%d %H:%M:%S')
        om.put(dates, date, sighting)
    return map


def requirement1(catalog, city):
    """
    Arma la respuesta del requisito 1 usando el árbol del requisito 1.
    """
    sample = lt.newList(datastructure='ARRAY')
    tree_req1 = catalog['req1']
    entry_tree_cities = om.get(tree_req1, city)
    tree_cities = me.getValue(entry_tree_cities)
    total = om.size(tree_cities)
    min_ = om.minKey(tree_cities)
    second = om.select(tree_cities, 1)
    third = om.select(tree_cities, 2)
    max_ = om.maxKey(tree_cities)
    second_to_last = om.select(tree_cities, total-2)
    third_to_last = om.select(tree_cities, total-3)
    for i in min_, second, third, third_to_last, second_to_last, max_:
        entry_sighting = om.get(tree_cities, i)
        sighting = me.getValue(entry_sighting)
        lt.addLast(sample, sighting)
    return total, sample


def requirement2():
    pass


def requirement3():
    pass


# Requirement 4


def create_tree_req4(tree, sighting):
    """
    Crea el árbol del requisito 4.
    El árbol tiene como llaves las fechas de avistamientos y como valores
    arreglos con los avistamientos por fecha.
    """
    time = sighting["datetime"][:10]
    entry = om.get(tree, time)
    if entry is None:
        sightings_list = lt.newList('ARRAY_LIST')
    else:
        sightings_list = me.getValue(entry)
    lt.addLast(sightings_list, sighting)
    om.put(tree, time, sightings_list)
    return tree


def requirement4(catalog, fechaMin, fechaMax):
    res = om.values(catalog["req4"], fechaMin, fechaMax)
    return res


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


def compare_datetime(datetime1, datetime2):
    """
    Compara dos fechas con hora en el formato YYYY-MM-DD HH:MM:SS
    usando la libreria Datetime.
    """
    date1 = datetime.strptime(datetime1,
                              '%Y-%m-%d %H:%M:%S')
    date2 = datetime.strptime(datetime2,
                              '%Y-%m-%d %H:%M:%S')
    if date1 < date2:
        return -1
    return 0


def compareTime(sighting1, sighting2):
    """
    Compara dos fechas con hora en el formato YYYY-MM-DD
    usando la libreria Datetime.
    """
    datetime1 = datetime.strptime(sighting1,
                                  '%Y-%m-%d').date()
    datetime2 = datetime.strptime(sighting2,
                                  '%Y-%m-%d').date()
    # print(datetime1)
    if datetime1 == datetime2:
        return 0
    elif datetime1 > datetime2:
        return 1
    else:
        return -1


# Funciones de ordenamiento
