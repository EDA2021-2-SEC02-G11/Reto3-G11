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


def opcion3(catalog):
    return model.opcion3(catalog)


def requirement1(catalog, city):
    return model.requirement1(catalog, city)


def requirement2():
    return model.requirement2()


def requirement3():
    return model.requirement3()


def requirement4():
    return model.requirement4()


def requirement5():
    return model.requirement5()


def requirement6():
    return model.requirement6()