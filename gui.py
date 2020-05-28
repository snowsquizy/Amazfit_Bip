#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gui.py
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

from datetime import datetime
import d_base
import image
from base import MiBand2  # Class for MiBand2 however works with Amazfit Bip
from constants import ALERT_TYPES   # Constants used to communicate with Bip
import gi  # GUI Library import
gi.require_version("Gtk", "3.0")  # Sets Gtk Version to use
from gi.repository import Gtk  # Sets GUI to Gtk framework


testing = False


class guiWindow(Gtk.Window):
    def __init__(self, params):
        """
        Class to create a Gtk Window for my application
        ARGS:       params = Application deatils stored in sqlite3 database
                             List of application and device information
        RETURNS:    Nothing
        """
        Gtk.Window.__init__(self, title="Amazfit Bip Data Analytics Program")
        self.set_size_request(360, 720)
        self.set_resizable(False)
        self.set_icon_from_file('icon.svg')
        self.MAC = params[0].decode("utf-8")
        self.HOURS = params[6]
        self.batt_per = params[1]
        self.u_time = params[6]

        grid = Gtk.Grid()
        self.add(grid)

        self.label_plot = Gtk.Label(label="Plot Data")
        self.label_data = Gtk.Label(label="Metrics")
        self.label_batt = Gtk.Label(label="Battery %")
        self.label_utim = Gtk.Label(label="Last Download")
        self.butt_down = Gtk.Button(label="Download Data from Amazfit Bip")
        self.butt_expo = Gtk.Button(label="Export Data to CSV File")
        self.butt_pl_day = Gtk.Button(label="Plot Daily")
        self.butt_pl_wee = Gtk.Button(label="Plot Weekly")
        self.butt_pl_mon = Gtk.Button(label="Plot Monthly")
        self.butt_pl_cus = Gtk.Button(label="Plot")
        self.butt_da_day = Gtk.Button(label="Data Daily")
        self.butt_da_wee = Gtk.Button(label="Data Weekly")
        self.butt_da_mon = Gtk.Button(label="Data Monthly")
        self.butt_da_cus = Gtk.Button(label="Data")
        self.butt_setup = Gtk.Button(label="Setup Device")
        self.butt_exit = Gtk.Button(label="Exit")
        self.entry_pl_cus = Gtk.Entry()
        self.entry_pl_cus.set_text(str(self.HOURS))
        self.entry_pl_cus.set_width_chars(6)
        self.entry_da_cus = Gtk.Entry()
        self.entry_da_cus.set_text(str(self.HOURS))
        self.entry_da_cus.set_width_chars(6)
        self.display_area = Gtk.Image()
        image.create_start_image(params[7])
        self.display_area.set_from_file("blank.png")

        self.butt_down.connect("clicked", self.on_butt_getData)
        self.butt_expo.connect("clicked", self.on_butt_export)
        self.butt_pl_day.connect("clicked", self.on_butt_plot, 24)
        self.butt_pl_wee.connect("clicked", self.on_butt_plot, 168)
        self.butt_pl_mon.connect("clicked", self.on_butt_plot, 672)
        self.butt_pl_cus.connect("clicked", self.on_butt_plot_cus)
        self.butt_da_day.connect("clicked", self.on_butt_data, 24)
        self.butt_da_wee.connect("clicked", self.on_butt_data, 168)
        self.butt_da_mon.connect("clicked", self.on_butt_data, 672)
        self.butt_da_cus.connect("clicked", self.on_butt_data_cus)
        self.butt_setup.connect("clicked", self.on_butt_setup)
        self.butt_exit.connect("clicked", Gtk.main_quit)

        grid.attach(self.butt_down, 0, 1, 6, 1)
        grid.attach(self.butt_expo, 0, 2, 6, 1)
        grid.attach(self.label_plot, 0, 3, 2, 2)
        grid.attach(self.butt_pl_day, 2, 3, 2, 1)
        grid.attach(self.butt_pl_wee, 4, 3, 2, 1)
        grid.attach(self.butt_pl_mon, 2, 4, 2, 1)
        grid.attach(self.entry_pl_cus, 4, 4, 1, 1)
        grid.attach(self.butt_pl_cus, 5, 4, 1, 1)
        grid.attach(self.label_data, 0, 5, 2, 2)
        grid.attach(self.butt_da_day, 2, 5, 2, 1)
        grid.attach(self.butt_da_wee, 4, 5, 2, 1)
        grid.attach(self.butt_da_mon, 2, 6, 2, 1)
        grid.attach(self.entry_da_cus, 4, 6, 1, 1)
        grid.attach(self.butt_da_cus, 5, 6, 1, 1)
        grid.attach(self.label_batt, 0, 7, 3, 1)
        grid.attach(self.label_utim, 3, 7, 3, 1)
        grid.attach(self.butt_setup, 0, 8, 3, 1)
        grid.attach(self.butt_exit, 3, 8, 3, 1)
        grid.attach(self.display_area, 0, 9, 6, 6)

    def on_butt_getData(self, widget):
        """
        On button click a MiBand2 object is created and feed the MAC address.
        This then connects to device, downloads data from last update and
        then stores in database.
        ARGS:       None
        Returns:    None
        """
        if testing:
            print("Downloading")
        band = MiBand2(self.MAC, debug=False)
        band.setSecurityLevel(level="medium")
        band.authenticate()
        band._auth_previews_data_notif(True)
        ts = d_base.get_para('u_time')
        start_time = (
            datetime.utcfromtimestamp(ts).strftime("%d.%m.%Y %H:%M"))
        start_time = datetime.strptime(start_time, "%d.%m.%Y %H:%M")
        if testing:
            print("Getting Data")
        band.start_get_previews_data(start_time)
        while band.active:
            band.waitForNotifications(0.1)
        band.send_alert(ALERT_TYPES.MESSAGE)
        band.disconnect()
        if testing:
            print("Download Complete")

    def on_butt_export(self, widget):
        if testing:
            print("Exporting")
        d_base.get_all_data()
        if testing:
            print("Exported")

    def on_butt_plot_cus(self, button):
        hours = self.entry_pl_cus.get_text()
        if testing:
            print("Plotting {} hours".format(hours))
        image.create_plot_image(int(hours))
        self.display_area.set_from_file("plots.png")
        d_base.set_para("hours", self.entry_pl_cus.get_text())

    def on_butt_plot(self, button, hours):
        if testing:
            print("Plotting {} hours".format(hours))
        image.create_plot_image(hours)
        self.display_area.set_from_file("plots.png")

    def on_butt_data_cus(self, button):
        hours = self.entry_da_cus.get_text()
        if testing:
            print("Data Extract {} hours".format(hours))
        image.create_data_image(int(hours))
        self.display_area.set_from_file("data.png")
        d_base.set_para("hours", self.entry_da_cus.get_text())

    def on_butt_data(self, button, hours):
        if testing:
            print("Data Extract {} hours".format(hours))
        image.create_data_image(hours)
        self.display_area.set_from_file("data.png")

    def on_butt_setup(self, widget):
        if testing:
            print("Setup")

