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
import folium as fo
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
                                comparefunction=compare_keys)
    catalog['req3'] = om.newMap(omaptype='RBT',
                                comparefunction=compare_hours)
    catalog['req4'] = om.newMap(omaptype='RBT',
                                comparefunction=compareTime)
    catalog['req5'] = om.newMap(omaptype='RBT',
                                comparefunction=compare_keys)

    return catalog


# Funciones para agregar información al catálogo


def add_sighting(catalog, sighting):
    lt.addLast(catalog['sightings'], sighting)  # Load data
    create_tree_req1(catalog['req1'], sighting)  # Requirement 1
    create_tree_req2(catalog['req2'], sighting)  # Requirement 2
    create_tree_req3(catalog['req3'], sighting)  # Requirement 3
    create_tree_req4(catalog['req4'], sighting)  # Requirement 4
    create_tree_req5(catalog['req5'], sighting)  # Requirement 5
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
    most_city = "ciudad"
    n_most_city = 0
    valores=om.valueSet(tree_req1)
    ciudades=om.keySet(tree_req1)
    print(lt.size(valores))
    print(lt.iterator(valores))
    pos=1
    while pos<=lt.size(valores):
        num=lt.getElement(valores,pos)["root"]["size"]
        if num>n_most_city:
            most_city=lt.getElement(ciudades,pos)
            n_most_city=num
        pos+=1
    return total_cities, total, sample, most_city, n_most_city


# Requirement 2


def create_tree_req2(tree_req2, sighting):
    """
    Crea el árbol del requisito 2.
    El árbol tiene como llaves duraciones en segundos y como valores árboles.
    Cada árbol tiene como llaves cadenas de caracteres de forma 'ciudad-zz',
    donde zz representa el acrónimo del país, y como valores arreglos con todos
    los avistamientos de dicha duración en segundos que ocurrieron en el país y
    ciudad dados. Para los que no tienen país se pone 'zz'.
    Nótese que en los datos ocurre que hay varios avistamientos con igual
    duración en segundos que ocurrieron en la misma ciudad.
    """
    entry = om.get(tree_req2, float(sighting['duration (seconds)']))
    if entry is None:
        zz_tree = om.newMap(omaptype='RBT', comparefunction=compare_keys)
        sightings_list = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(sightings_list, sighting)
        om.put(zz_tree, zz_key(sighting), sightings_list)
        om.put(tree_req2, float(sighting['duration (seconds)']), zz_tree)
    else:
        zz_tree = me.getValue(entry)
        zz_tree_entry = om.get(zz_tree, zz_key(sighting))
        if zz_tree_entry is None:
            sightings_list = lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(sightings_list, sighting)
            om.put(zz_tree, zz_key(sighting), sightings_list)
        else:
            lt.addLast(me.getValue(zz_tree_entry), sighting)
    return tree_req2


def zz_key(sighting):
    """
    Retorna una cadena de caracteres con el formato 'ciudad-zz' donde zz
    representa el acrónimo del país, para un avistamiento dado.
    Para los que no tienen país se pone 'zz' como acrónimo del país.
    """
    country = sighting['country'].strip()
    if country == '':
        country = 'zz'
    city = sighting['city'].strip()
    llave = city+'-'+country
    return llave


def requirement2(catalog, sec_min, sec_max):
    """
    Arma la respuesta del requisito 2 usando el árbol del requisito 2.
    """
    # Longest sightings
    tree_req2 = catalog['req2']
    total_durations = om.size(tree_req2)
    top_duration = om.maxKey(tree_req2)
    country_city_entry_top = om.get(tree_req2, top_duration)
    country_city_tree_top = me.getValue(country_city_entry_top)
    count_top_duration = om.size(country_city_tree_top)

    # Top 3 and last 3
    sample = lt.newList(datastructure='ARRAY_LIST')
    n_range = 0
    range_duration = om.values(tree_req2, sec_min, sec_max)

    """ Este ciclo añade los tres primeros avistamientos. Nótese que el ciclo
    corre como máximo tres veces."""
    i1 = 1
    while lt.size(sample) < 3 and i1 <= lt.size(range_duration):
        zz_tree = lt.getElement(range_duration, i1)
        values_zz_tree = om.valueSet(zz_tree)
        i1 += 1
        j1 = 1
        while lt.size(sample) < 3 and j1 <= lt.size(values_zz_tree):
            sightings_list = lt.getElement(values_zz_tree, j1)
            j1 += 1
            k1 = 1
            while lt.size(sample) < 3 and k1 <= lt.size(sightings_list):
                sighting = lt.getElement(sightings_list, k1)
                lt.addLast(sample, sighting)
                k1 += 1

    """ Este ciclo añade los tres últimos avistamientos. Nótese que, al igual
    que el ciclo anterior, corre máximo tres veces."""
    i2 = lt.size(range_duration)
    while lt.size(sample) >= 3 and lt.size(sample) < 6 and i2 >= i1:
        zz_tree = lt.getElement(range_duration, i2)
        values_zz_tree = om.valueSet(zz_tree)
        i2 -= 1
        j2 = lt.size(values_zz_tree)
        while lt.size(sample) >= 3 and lt.size(sample) < 6 and j2 >= 1:
            sightings_list = lt.getElement(values_zz_tree, j2)
            j2 -= 1
            k2 = lt.size(sightings_list)
            while lt.size(sample) >= 3 and lt.size(sample) < 6 and k2 >= 1:
                sighting = lt.getElement(sightings_list, k2)
                lt.addLast(sample, sighting)
                k2 -= 1

    """ Este último ciclo cuenta el número de avistamientos en el rango. El
    número de veces que corre depende del rango dado."""
    for zz_tree in lt.iterator(range_duration):
        for sightings_list in lt.iterator(om.valueSet(zz_tree)):
            n_range += lt.size(sightings_list)
    return total_durations, top_duration, count_top_duration, n_range, sample


# Requirement 3


def create_tree_req3(tree, sighting):
    """
    Crea el árbol del requisito 3.
    El árbol tiene como llaves las horas de avistamientos y como valores
    arreglos con los avistamientos por fecha en una lista.
    """
    time = sighting["datetime"][11:]
    entry = om.get(tree, time)
    if entry is None:
        sightings_list = lt.newList('ARRAY_LIST')
    else:
        sightings_list = me.getValue(entry)
    lt.addLast(sightings_list, sighting)
    om.put(tree, time, sightings_list)
    return tree


def requirement3(catalog, horaMin, horaMax):
    """
    Arma la respuesta del requisito 3 usando el árbol del requisito 3.
    """
    tree_req3 = catalog["req3"]
    total_dates = om.size(tree_req3)
    oldest = om.maxKey(tree_req3)
    entry_oldest = om.get(tree_req3, oldest)
    oldest_array = me.getValue(entry_oldest)
    n_oldest = lt.size(oldest_array)
    range_values = om.values(tree_req3, horaMin, horaMax)
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


def create_tree_req5(tree_req5, sighting):
    """
    Crea el árbol del requisito 5.
    El árbol tiene como llaves la coordenada latitud (aproximada a dos cifras
    decimales) y como valores árboles. Cada árbol tiene como llaves
    coordenadas de longitud (aproximadas a dos cifras decimales) y como valores
    arreglos con todos los avistamientos que tomaron lugar en la latitud y
    longitud dada.
    Nótese que en los datos ocurre que ocurrieron en exactamente la misma
    latitud y longitud.
    """
    entry = om.get(tree_req5, rf(sighting['latitude']))
    if entry is None:
        long_tree = om.newMap(omaptype='RBT', comparefunction=compare_keys)
        sightings_list = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(sightings_list, sighting)
        om.put(long_tree, rf(sighting['longitude']), sightings_list)
        om.put(tree_req5, rf(sighting['latitude']), long_tree)
    else:
        long_tree = me.getValue(entry)
        long_tree_entry = om.get(long_tree, rf(sighting['longitude']))
        if long_tree_entry is None:
            sightings_list = lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(sightings_list, sighting)
            om.put(long_tree, rf(sighting['longitude']), sightings_list)
        else:
            lt.addLast(me.getValue(long_tree_entry), sighting)
    return tree_req5


def rf(coordinate):
    return round(float(coordinate), 2)


def requirement5(catalog, lon_min, lon_max, lat_min, lat_max):
    """
    Arma la respuesta del requisito 5 usando el árbol del requisito 5.
    """
    tree_req5 = catalog['req5']
    sample = lt.newList(datastructure='ARRAY_LIST')
    n_range = 0
    range_lat = om.values(tree_req5, lat_min, lat_max)

    """ Este ciclo añade los cinco primeros avistamientos. Nótese que el ciclo
    corre como máximo cinco veces."""
    i1 = 1
    while lt.size(sample) < 5 and i1 <= lt.size(range_lat):
        lon_tree = lt.getElement(range_lat, i1)
        values_lon_tree = om.values(lon_tree, lon_min, lon_max)
        i1 += 1
        j1 = 1
        while lt.size(sample) < 5 and j1 <= lt.size(values_lon_tree):
            sightings_list = lt.getElement(values_lon_tree, j1)
            j1 += 1
            k1 = 1
            while lt.size(sample) < 5 and k1 <= lt.size(sightings_list):
                sighting = lt.getElement(sightings_list, k1)
                lt.addLast(sample, sighting)
                k1 += 1

    """ Este ciclo añade los cinco últimos avistamientos. Nótese que, al igual
    que el ciclo anterior, corre máximo cinco veces."""
    i2 = lt.size(range_lat)
    while lt.size(sample) >= 5 and lt.size(sample) < 10 and i2 >= i1:
        lon_tree = lt.getElement(range_lat, i2)
        values_lon_tree = om.values(lon_tree, lon_min, lon_max)
        i2 -= 1
        j2 = lt.size(values_lon_tree)
        while lt.size(sample) >= 5 and lt.size(sample) < 10 and j2 >= 1:
            sightings_list = lt.getElement(values_lon_tree, j2)
            j2 -= 1
            k2 = lt.size(sightings_list)
            while lt.size(sample) >= 5 and lt.size(sample) < 10 and k2 >= 1:
                sighting = lt.getElement(sightings_list, k2)
                lt.addLast(sample, sighting)
                k2 -= 1

    """ Este último ciclo cuenta el número de avistamientos en el rango. El
    número de veces que corre depende del rango dado."""
    for lon_tree in lt.iterator(range_lat):
        for s_list in lt.iterator(om.values(lon_tree, lon_min, lon_max)):
            n_range += lt.size(s_list)
    return sample, n_range


# Requirement 6


def requirement6(catalog, lon_min, lon_max, lat_min, lat_max):
    sample, n_range = requirement5(catalog, lon_min, lon_max, lat_min, lat_max)
    origen = round((lat_max+lat_min)/2), round((lon_max+lon_min)/2)
    mapa = fo.Map(location=origen, tiles='Stamen Toner', zoom_start=7)
    fo.Rectangle(bounds=[[lat_min, lon_min], [lat_max, lon_max]],
                 color='green', fill=True, fill_color='green',
                 fill_opacity=0.1).add_to(mapa)
    for i in range(1, lt.size(sample)+1):
        lat = float(lt.getElement(sample, i)['latitude'])
        lon = float(lt.getElement(sample, i)['longitude'])
        h1 = str(lt.getElement(sample, i)['datetime'][:10])
        h2 = str(lt.getElement(sample, i)['datetime'][11:])
        h3 = str(lt.getElement(sample, i)['city'].title())
        h4 = str(lt.getElement(sample, i)['country'].title())
        h5 = str(lt.getElement(sample, i)['duration (seconds)'])
        h6 = str(lt.getElement(sample, i)['shape'])
        h7 = str(float(lt.getElement(sample, i)['latitude']))
        h8 = str(float(lt.getElement(sample, i)['longitude']))
        html_table = ('<b>Date: </b>'+h1 +
                      '<br><b>Time: </b>'+h2 +
                      '<br><b>City: </b>'+h3 +
                      '<br><b>Country: </b>'+h4 +
                      '<br><b>Duration: </b>'+h5+' s' +
                      '<br><b>Shape: </b>'+h6 +
                      '<br><b>Latitude: </b>'+h7 +
                      '<br><b>Longitude: </b>'+h8)
        if i == 1:
            muestre = True
        else:
            muestre = False
        popup_ = fo.Popup(html=html_table, min_width=150, max_width=200,
                          show=muestre)
        fo.Marker(location=[lat, lon], popup=popup_,
                  icon=fo.Icon(color="red", icon="cloud")).add_to(mapa)
    mapa.save("requerimiento6.html")
    guardo = True
    return n_range, sample, guardo


# Comparing functions


def compare_keys(key1, key2):
    """
    Compara dos cosas cualquiera.
    """
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


def compare_hours(sighting1, sighting2):
    """
    Compara dos horas en el formato
    usando la libreria Datetime.
    """
    datetime1 = datetime.strptime(sighting1,
                                  '%H:%M:%S').time()
    datetime2 = datetime.strptime(sighting2,
                                  '%H:%M:%S').time()
    # print(datetime1)
    if datetime1 == datetime2:
        return 0
    elif datetime1 > datetime2:
        return 1
    else:
        return -1


def compare_latitude(sighting1, sighting2):
    latitud1 = round(float(sighting1["latitude"]), 2)
    latitud2 = round(float(sighting2["latitude"]), 2)
    return compare_keys(latitud1, latitud2)
