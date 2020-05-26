#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  bip_btle.py
#
#  Copyright 2020 Andrew Taylor <andrew@snowsquizy.id.au>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

'''Gtk Main Program to connect to Amazfit Bip btle smartwatch,
initialise the connection, retreive data, store it within a sqlite3
database, export to csv file, plot data over time and display
calculated metrics.
'''

# Library Imports
from datetime import datetime  # Display and fetch date time values
from constants import ALERT_TYPES  # Constants for connection
import os  # for confirming database file and deleting images on quit
from gui import *  # Gtk Window Class
import image


def main():
    info = [
        'mac_add',
        'battery',
        'soft_ver',
        'hard_rev',
        'ser_num',
        'u_time',
        'hours',
        's_image']
    params = []
    for i in range(len(info)):
        params.append(d_base.get_para(info[i]))
    win = guiWindow(params)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    image.clean_up()


if __name__ == '__main__':
    main()
