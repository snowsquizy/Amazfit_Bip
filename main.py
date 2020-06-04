#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
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
import gui  # Tkinter Window Class
import image  # for file cleanup on exit
import d_base
from tkinter import *


def main():
    """
    Main Application Method
    ARGS:       None
    RETURNS:    None
    """
    root = Tk()
    app = gui.Window(root)
    root.wm_title("Amazfit Bip Interface")
    root.geometry("360x700")
    root.mainloop()
    image.clean_up()


if __name__ == '__main__':
    main()
