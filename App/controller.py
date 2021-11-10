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
 """


import config as cf
import model
import csv


def init_catalog():
    catalog = model.new_catalog()
    return catalog


def load_data(catalog):
    file = cf.data_dir + 'UFOS/UFOS-utf8-small.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for sighting in input_file:
        model.add_sighting(catalog, sighting)


def requirement1(catalog, city):
    return model.requirement1(catalog, city)


def requirement2(catalog, sec_min, sec_max):
    return model.requirement2(catalog, sec_min, sec_max)


def requirement3(catalog, horaMin, horaMax):
    return model.requirement3(catalog, horaMin, horaMax)


def requirement4(catalog, fechaMin, fechaMax):
    return model.requirement4(catalog, fechaMin, fechaMax)


def requirement5(catalog, lon_min, lon_max, lat_min, lat_max):
    return model.requirement5(catalog, lon_min, lon_max, lat_min, lat_max)


def requirement6():
    return model.requirement6()
