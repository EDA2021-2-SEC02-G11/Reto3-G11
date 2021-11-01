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

    catalog['sightings'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['req1'] = om.newMap(omaptype='RBT',
                                comparefunction=compare_keys)
    catalog['req2'] = om.newMap(omaptype='RBT',
                                comparefunction=compare_durations)
    catalog['req4'] = om.newMap(omaptype='RBT',
                                comparefunction=compareTime)

    return catalog


# Funciones para agregar información al catalogo


def add_sighting(catalog, sighting):
    lt.addLast(catalog['sightings'], sighting)  # Load data
    create_tree_req1(catalog['req1'], sighting)  # Requirement 1
    create_tree_req2(catalog['req2'], sighting)  # Requirement 2
    create_tree_req4(catalog['req4'], sighting)  # Requirement 4
    return catalog


# Requirement 1


def create_tree_req1(tree_req1, sighting):
    """
    Crea el árbol del requisito 1.
    El árbol tiene como llaves ciudades y como valores árboles.
    Cada árbol tiene como llaves fechas (con hora, en formato datetime) y el
    valor correspondiente a cada llave es el avistamiento en la ciudad dada a
    la fecha y hora de la llave.
    Nótese que en los datos no hay dos avistamientos que hayan ocurrido en la
    misma ciudad y en la misma fecha, hora, minuto y segundo.
    """
    entry = om.get(tree_req1, sighting['city'])
    if entry is None:
        dates = om.newMap(omaptype='RBT',
                          comparefunction=compare_keys)
        date = datetime.strptime(sighting['datetime'],
                                 '%Y-%m-%d %H:%M:%S')
        om.put(dates, date, sighting)
        om.put(tree_req1, sighting['city'], dates)
    else:
        dates = me.getValue(entry)
        date = datetime.strptime(sighting['datetime'],
                                 '%Y-%m-%d %H:%M:%S')
        om.put(dates, date, sighting)
    return tree_req1


def requirement1(catalog, city):
    """
    Arma la respuesta del requisito 1 usando el árbol del requisito 1.
    """
    sample = lt.newList(datastructure='ARRAY')
    tree_req1 = catalog['req1']
    total_cities = om.size(tree_req1)
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
    return total_cities, total, sample


# Requirement 2


def create_tree_req2(tree_req2, sighting):
    """
    Crea el árbol del requisito 2.
    El árbol tiene como llaves duraciones en segundos y como valores árboles.
    Cada árbol tiene como llaves cadenas de caracteres de forma 'zz-ciudad',
    donde zz representa el acrónimo del país, y como valores arreglos con todos
    los avistamientos de dicha duración en segundos que ocurrieron en el país y
    ciudad dados. Para los que no tienen país se pone 'zz'.
    Nótese que en los datos ocurre que hay varios avistamientos con igual
    duración en segundos que ocurrieron en la misma ciudad.
    """
    entry = om.get(tree_req2, sighting['duration (seconds)'])
    if entry is None:
        countries_cities = om.newMap(omaptype='RBT',
                                     comparefunction=compare_keys)
        country_city = country_city_key(sighting)
        om.put(countries_cities, country_city, sighting)
        om.put(tree_req2, sighting['duration (seconds)'], countries_cities)
    else:
        countries_cities = me.getValue(entry)
        country_city = country_city_key(sighting)
        om.put(countries_cities, country_city, sighting)
    return tree_req2


def country_city_key(sighting):
    """
    Retorna una cadena de caracteres con el formato 'zz-ciudad' donde zz
    representa el acrónimo del país, para un avistamiento dado.
    Para los que no tienen país se pone 'zz' como acrónimo del país.
    """
    country = sighting['country'].strip()
    if country == '':
        country = 'zz'
    city = sighting['city'].strip()
    llave = country+'-'+city
    return llave


def requirement2(catalog, sec_min, sec_max):
    # sample = lt.newList(datastructure='ARRAY')
    tree_req2 = catalog['req2']
    total_durations = om.size(tree_req2)
    top_duration = om.maxKey(tree_req2)
    country_city_entry_top = om.get(tree_req2, top_duration)
    country_city_tree_top = me.getValue(country_city_entry_top)
    count_top_duration = om.size(country_city_tree_top)
    # TODO: for para 3 top 3 last
    return total_durations, top_duration, count_top_duration


# Requirement 3


def create_tree_req3(tree, sighting):
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
    tree_req4 = catalog["req4"]
    total_dates = om.size(tree_req4)
    oldest = om.minKey(tree_req4)
    entry_oldest = om.get(tree_req4, oldest)
    oldest_array = me.getValue(entry_oldest)
    n_oldest = lt.size(oldest_array)
    range_values = om.values(tree_req4, fechaMin, fechaMax)
    rango = lt.newList(datastructure='ARRAY_LIST')
    n_rango = 0
    rango_for = lt.size(range_values)
    for i in range(1, rango_for+1):
        sightings_array = lt.getElement(range_values, i)
        if i in (1, 2, 3, rango_for-2, rango_for-1, rango_for):
            if lt.size(sightings_array) <= 1:
                sighting = lt.getElement(sightings_array, 1)
                lt.addLast(rango, sighting)
                n_rango += lt.size(sightings_array)
            else:
                for sighting in lt.iterator(sightings_array):
                    n_rango += 1
                    lt.addLast(rango, sighting)
        else:
            n_rango += lt.size(sightings_array)
    return total_dates, oldest, n_oldest, n_rango, rango


# Requirement 5


def create_tree_req5(tree, sighting):
    pass


def requirement5():
    pass


# Requirement 6


def create_tree_req6(tree, sighting):
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


def compare_durations(duration1, duration2):
    """
    Compara dos duraciones que entran como cadenas de caracteres.
    """
    key1 = float(duration1)
    key2 = float(duration2)
    if key1 == key2:
        return 0
    elif key1 > key2:
        return 1
    else:
        return -1


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
