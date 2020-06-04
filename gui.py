#!/usr/bin/env python3
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

from tkinter import *  # GUI framwework
import os  # Getting current working directory for files
from datetime import datetime  # for controlling time
import d_base  # Working with the databases
import image  # Creating the start images, plots and data extracts
from base import MiBand2  # Class for MiBand2 however works with Amazfit Bip
from constants import ALERT_TYPES   # Constants used to communicate with Bip

# Variables
testing = False


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.info = [
            'file_name', 't_schema', 'mac_add', 'battery',
            'soft_ver', 'hard_ver', 'ser_num', 'u_time',
            'hours', 's_image', 'a_icon']
        params = []
        pwd = os.getcwd()
        for i in range(len(self.info)):
            params.append(d_base.get_para(self.info[i]))
        self.db_name = pwd + '/' + params[0].decode('utf-8')
        self.schema = params[1].decode('utf-8')
        self.MAC = params[2].decode('utf-8')
        self.battery = params[3]
        self.soft_ver = params[4].decode('utf-8')
        self.hard_ver = params[5].decode('utf-8')
        self.ser_num = params[6].decode('utf-8')
        self.u_time = params[7]
        self.HOURS = params[8]
        self.s_image = params[9]
        self.a_icon = params[10]
        image.create_start_images(self.s_image, self.a_icon)
        self.tvplot = StringVar()
        self.dvdata = StringVar()
        self.battery_label_text = StringVar()
        self.time_u = StringVar()

        # Download Button
        download_button = Button(
            self.master, text="Download Data from Amazfit Bip", borderwidth=1,
            command=self.getData).grid(row=0, columnspan=6, sticky='NESW')

        # Export Button
        export_button = Button(
            self.master, text="Export all Data to CSV File", borderwidth=1,
            command=self.exportData).grid(row=1, columnspan=6, sticky='NESW')

        # Plot Label
        plot_label = Label(self.master, text="Plots", borderwidth=1)
        plot_label.grid(row=2, column=0, columnspan=2, rowspan=2, sticky='NESW')

        # Plot Daily Data
        plot_daily_button = Button(
            self.master, text="Plot Daily", borderwidth=1,
            command=lambda: self.plot(24)).grid(row=2, column=2, columnspan=2, sticky='NESW')

        # Plot Daily Weekly
        plot_weekly_button = Button(
            self.master, text="Plot Weekly", borderwidth=1,
            command=lambda: self.plot(168)).grid(row=2, column=4, columnspan=2, sticky='NESW')

        # Plot Monthly Data
        plot_monthly_button = Button(
            self.master, text="Plot Monthly", borderwidth=1,
            command=lambda: self.plot(672)).grid(row=3, column=2, columnspan=2, sticky='NESW')

        # Custom Plot Value
        custom_entry_plot = Entry(
            self.master, width=4, textvariable=self.tvplot).grid(row=3, column=4, sticky='NESW')
        self.tvplot.set(d_base.get_para('hours'))

        # Plot Custom Button
        plot_custom_button = Button(
            self.master, text="Plot", borderwidth=1,
            command=lambda: self.plot(int(self.tvplot.get()))).grid(row=3, column=5, sticky='NESW')

        # Data Label
        data_label = Label(self.master, text="Data", borderwidth=1)
        data_label.grid(row=4, column=0, columnspan=2, rowspan=2, sticky='NESW')

        # Data Daily
        data_daily_button = Button(
            self.master, text="Data Daily", borderwidth=1,
            command=lambda: self.data(24)).grid(row=4, column=2, columnspan=2, sticky='NESW')

        # Data Weekly, borderwidth=1
        data_weekly_button = Button(
            self.master, text="Data Weekly", borderwidth=1,
            command=lambda: self.data(168)).grid(row=4, column=4, columnspan=2, sticky='NESW')

        # Data Monthly
        data_monthly_button = Button(
            self.master, text="Data Monthly", borderwidth=1,
            command=lambda: self.data(672)).grid(row=5, column=2, columnspan=2, sticky='NESW')

        # Custom Data Value
        self.custom_entry_data = Entry(
            self.master, width=4, textvariable=self.dvdata).grid(row=5, column=4, sticky='NESW')
        self.dvdata.set(d_base.get_para('hours'))

        # Data Custom button
        plot_custom_button = Button(
            self.master, text="Data", borderwidth=1,
            command=lambda: self.data(int(self.dvdata.get()))).grid(row=5, column=5, sticky='NESW')

        # Battery Percentage Label
        battery_label1 = Label(self.master, text="Battery:-", borderwidth=1)
        battery_label1.grid(row=6, sticky='NESW')

        # Battery Percentage Value
        battery_label2 = Label(
            self.master, textvariable=self.battery_label_text, borderwidth=1)
        battery_label2.grid(row=6, column=1, sticky='NESW')
        self.battery_label_text.set("{}%".format(self.battery))

        # Last Update Time Label
        utime1_label = Label(self.master, text="Last Update :-", borderwidth=1)
        utime1_label.grid(row=6, column=2, columnspan=2, sticky='NESW')

        # Last Update Time Value
        time_new = datetime.fromtimestamp(self.u_time + 43200).strftime('%Y-%m-%d %H:%M')
        self.utime2_label = Label(
            self.master, textvariable=self.time_u, borderwidth=1)
        self.utime2_label.grid(row=6, column=4, columnspan=2, sticky="NESW")
        self.time_u.set(time_new)
        
        # Image area setup
        render = PhotoImage(file="blank.png")
        self.image_label = Label(self.master, image=render, borderwidth=1)
        self.image_label.image = render
        self.image_label.grid(row=7, columnspan=6, rowspan=12, sticky="NESW")

        # Setup Window Button
        setup_button = Button(
            self.master, text="Setup Program",
            command=self.setup_window).grid(row=19, columnspan=3, sticky="NESW")

        # Exit Button
        Button(
            self.master, text="Exit program",
            command=self.master.quit).grid(row=19, column=3, columnspan=3, sticky="NESW")

        col_count, row_count = self.master.grid_size()
        for i in range(col_count):
            self.master.grid_columnconfigure(i, minsize=60)
        for j in range(row_count):
            self.master.grid_rowconfigure(j, minsize=35)

    def getData(self):
        """
        On button click a MiBand2 object is created and feed the MAC address.
        This then connects to device, downloads data from last update and
        then stores in database. Updates Properties of watch in Datbase
        ARGS:       None
        Returns:    None
        """
        if testing:
            print("Downloading")
        band = MiBand2(self.MAC, debug=False)
        band.setSecurityLevel(level="medium")
        band.authenticate()
        band._auth_previews_data_notif(True)
        start_time = (
            datetime.utcfromtimestamp(self.u_time).strftime("%d.%m.%Y %H:%M"))
        start_time = datetime.strptime(start_time, "%d.%m.%Y %H:%M")
        if testing:
            print("Getting Data")
        band.start_get_previews_data(start_time)
        while band.active:
            band.waitForNotifications(0.1)
        d_base.set_para('battery', band.get_battery_info()['level'])
        d_base.set_para('soft_ver', band.get_revision())
        d_base.set_para('hard_ver', band.get_hrdw_revision())
        d_base.set_para('ser_num', band.get_serial())
        band.send_alert(ALERT_TYPES.MESSAGE)
        band.disconnect()
        self.battery_label_text.set("{}%".format(d_base.get_para('battery')))
        time_new = datetime.fromtimestamp(d_base.get_para('u_time') + 43200).strftime('%Y-%m-%d %H:%M')
        self.time_u.set(time_new)
        if testing:
            print("Download Complete")

    def exportData(self):
        """
        On button click the entire database of data is exported to a CSV
        file with filename 'export DTG.csv'
        ARGS:       None
        RETURNS:    None
        """
        if testing:
            print("Exporting")
        d_base.get_all_data()
        if testing:
            print("Exported")

    def plot(self, hours):
        if testing:
            print("Plotting {} Hours".format(hours))
        image.create_plot_image(hours)
        render = PhotoImage(file="plots.png")
        self.image_label.configure(image=render)
        self.image = render
        d_base.set_para('hours', hours)
        if testing:
            print("Plotting Complete")

    def data(self, hours):
        if testing:
            print("Extracting {} Hours Data".format(hours))
        image.create_data_image(hours)
        render = PhotoImage(file="data.png")
        self.image_label.configure(image=render)
        self.image = render
        d_base.set_para('hours', hours)
        if testing:
            print("Data Extracted")

    def setup_window(self):
        if testing:
            print("Setup Window Opening")
        setup_Win = Toplevel(width=360, height=360)
        setup_Win.wm_title("Amazfit Bip Setup")
        MAC = d_base.get_para('mac_add').decode('utf-8')
        self.c_mac = StringVar()
        # MAC Address Label
        mac_add_label = Label(setup_Win, text="MAC Address:-", borderwidth=1)
        mac_add_label.grid(row=0, column=0, sticky='NESW')
        # Mac Address Value
        mac_add_value = Entry(setup_Win, width=17, textvariable=self.c_mac)
        mac_add_value.grid(row=0, column=1, sticky='NESW')
        self.c_mac.set(MAC)
        # Software Version Label
        soft_ver_label = Label(setup_Win, text="Software Revision :-", borderwidth=1)
        soft_ver_label.grid(row=1, column=0, sticky='NESW')
        # Software Version Value
        soft_ver_value = Label(setup_Win, text=d_base.get_para('soft_ver'), borderwidth=1)
        soft_ver_value.grid(row=1, column=1, sticky='NESW')
        # Hardware Version Label
        hard_ver_label = Label(setup_Win, text="Hardware Revision :-", borderwidth=1)
        hard_ver_label.grid(row=2, column=0, sticky='NESW')
        # Hardware Revision Value
        hard_ver_value = Label(setup_Win, text=d_base.get_para('hard_ver'), borderwidth=1)
        hard_ver_value.grid(row=2, column=1, sticky='NESW')
        # Serial Number Label
        ser_num_label = Label(setup_Win, text="Serial Number :-", borderwidth=1)
        ser_num_label.grid(row=3, column=0, sticky='NESW')
        # Serial Number Value
        ser_num_value = Label(setup_Win, text=d_base.get_para('ser_num'), borderwidth=1)
        ser_num_value.grid(row=3, column=1, sticky='NESW')
        # Warning Label
        warn_label = Label(setup_Win, text="This will wipe band data", borderwidth=1)
        warn_label.grid(row=4, column=0, sticky='NESW')
        # Initialise Button
        init_button = Button(setup_Win, text="Initialise Device", command=self.initialise_device)
        init_button.grid(row=4, column=1, sticky='NESW')
        # Exit Button
        exit_button = Button(setup_Win, text="Exit Setup",command=setup_Win.destroy)
        exit_button.grid(row=7, column=1, sticky="NESW")       
        
        col_count, row_count = setup_Win.grid_size()
        for i in range(col_count):
            setup_Win.grid_columnconfigure(i, minsize=180)
        for j in range(row_count):
            setup_Win.grid_rowconfigure(j, minsize=35)
        if testing:
            print("Setup Window Closed")

    def initialise_device(self):
        if testing:
            print("Initialising Device")
        MAC = self.c_mac.get()
        print(MAC)
        band = MiBand2(MAC, debug=False)
        band.setSecurityLevel(level="medium")
        #if band.initialize():
            #print("Init OK")
        band.set_heart_monitor_sleep_support(enabled=True)
        band.disconnect()
        d_base.set_para('mac_add', MAC)
        if testing:
            print("Initailisation Complete")
        self.destroy

    def update_destroy(self):
        if testing:
            print("Updating MAC address")
        MAC = self.c_mac.get()
        d_base.set_para('mac_add', MAC)
        if testing:
            print("closing window")
        self.destroy
