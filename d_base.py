#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  d_base.py
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

"""
Database methods used for bip_btle program to set and get data.
SQLITE3 Database schema

CREATE TABLE `fitness` (
    `d_t`	NUMERIC NOT NULL UNIQUE,
    `r_k`	INTEGER NOT NULL,
    `r_i`	INTEGER NOT NULL,
    `s_t`	INTEGER NOT NULL,
    `h_r`	INTEGER,
    PRIMARY KEY(`d_t`)
);
CREATE TABLE `parameters` (
    `id`	INTEGER NOT NULL,
    `mac_add`	NUMERIC,
    `battery`	INTEGER,
    `soft_ver`	NUMERIC,
    `hard_rev`	NUMERIC,
    `ser_num`	INTEGER,
    `u_time`	NUMERIC NOT NULL,
    `hours`	INTEGER NOT NULL,
    `s_image`	BLOB NOT NULL,
    PRIMARY KEY(`id`)
);

"""

# Library Imports
import sqlite3
from sqlite3 import Error
from datetime import datetime
import csv
import os

# Variables
testing = False
app_file_name = "app.db"
pwd = os.getcwd()
app_db = pwd + '/' + app_file_name
data_file_name = "fitness.db"
data_db = pwd + '/' + data_file_name


def get_para(c_name):
    """
    Connects to default Database and retreive application
    settings
    ARGS:       c_name = Colomn to get data from
    RETURNS:    row[0] = Id
                row[1] = appliaction db
                row[2] = table schema
                row[3] = MAC Address
                row[4] = battery percentage
                row[5] = software revision
                row[6] = hardware version
                row[7] = serial number
                row[8] = last update time
                row[9] = Hours Interval
                row[10] = Blank Image
                row[11] = App Icon
    """
    result = []
    try:
        conn = connect_DB(app_db)
        sql = conn.cursor()
        if testing:
            print("Cursor Created")
        sql_statement = "SELECT {} FROM parameters WHERE id = 1".format(c_name)
        sql.execute(sql_statement)
        row = sql.fetchone()
        result = row[0]
    except Error:
        print(
            "Error with SQLite retrieving app data {}".format(Error))
    finally:
        conn.close()
    return result


def set_para(c_name, n_value):
    """
    Connects to default Database and updates application values
    ARGS:       c_name = Column Name in DB
                n_value = value to place in colomn
    RETURNS     None
    """
    try:
        conn = connect_DB(app_db)
        sql = conn.cursor()
        if testing:
            print("Cursor Created")
        sql_statement = (
            "UPDATE parameters SET {} = (?) WHERE id = 1".format(c_name))
        sql.execute(sql_statement, (n_value,))
        conn.commit()
    except Error:
        print("Error while working with SQLite ", Error)
    finally:
        conn.close()


def get_watch_data(hours):
    """
    Method to return all data from Database from now back a number of hours
    ARGS:       hours - Hours back to fetch data
    RETURNS:    d_t - Unix time data
                r_k - Category data
                r_i - Intensity data
                s_t - Steps data
                h_r - Heart Rate data
    """
    d_t, r_k, r_i, s_t, h_r = ([] for i in range(5))
    date_now = int(datetime.now().timestamp())
    date_before = date_now - (hours * 60 * 60)
    try:
        conn = connect_DB(data_db)
        sql = conn.cursor()
        if testing:
            print("Cursor Created")
        sql_statement = """SELECT * FROM fitness
                        WHERE d_t > {}""".format(date_before)
        sql.execute(sql_statement)
        rows = sql.fetchall()
        for row in rows:
            d_t.append(row[0])
            r_k.append(row[1])
            r_i.append(row[2])
            s_t.append(row[3])
            h_r.append(row[4])
    except Error:
        print("Error while working with SQLite ", Error)
    finally:
        conn.close()
    return d_t, r_k, r_i, s_t, h_r


def store_watch_data(in_data):
    """
    Method to store data in sqlite3 database
    ARGS:       in_data = [(
                    unix_time,
                    category,
                    intensity,
                    steps,
                    heart_rate)]
    RETURNS:    None
    """
    update_utime = None
    try:
        conn = connect_DB(data_db)
        sql = conn.cursor()
        if testing:
            print("Cursor Created")
        sql_statement = """INSERT or IGNORE into fitness
                        (d_t, r_k, r_i, s_t, h_r) VALUES
                        (?, ?, ?, ?, ?)"""
        sql.executemany(sql_statement, in_data)
        if testing:
            print("Data Inserted")
        conn.commit()
        for item in in_data:
            update_utime = item[0]
        update_utime = int(update_utime) - 43200
        set_para('u_time', update_utime)
    except Error:
        print("Error while working with SQLite ", Error)
    finally:
        conn.close()


def get_all_data():
    """
    Method to export all Database information to CSV File
    ARGS:       None
    RETURNS:    file_n - File Name Created under
    """
    try:
        conn = connect_DB(data_db)
        sql = conn.cursor()
        if testing:
            print("Cursor Created")
        file_n = "export_{}.csv".format(datetime.now())
        with open(file_n, "w") as f_w:
            csv_out = csv.writer(f_w)
            for row in sql.execute("SELECT * FROM fitness"):
                csv_out.writerow(row)
    except Error:
        print("Error while working with SQLite ", Error)
    finally:
        conn.close()
        return file_n


def connect_DB(db_name):
    conn = sqlite3.connect(db_name)
    if testing:
        print("Connected to DB")
    conn.text_factory = bytes
    return conn


if testing:
    """
    Testing of the individual methods
    """
    set_para('mac_add', 'CA:0D:D7:A9:99:48')
    set_para("battery", 100)
    set_para("soft_ver", 100)
    set_para("hard_rev", 100)
    set_para("ser_num", 100)
    set_para("u_time", 100)
    set_para("hours", 100)
    print("*** Tested 'set_para' Method ***")

    print(get_para('id'))
    print(get_para('mac_add'))
    print(get_para("battery"))
    print(get_para("soft_ver"))
    print(get_para("hard_rev"))
    print(get_para("ser_num"))
    print(get_para("u_time"))
    print(get_para("hours"))
    print("*** Tested 'get_para' Method ***")

    store_watch_data([
        (1590408146, 1, 1, 1, 1),
        (1590408147, 2, 2, 2, 2),
        (1590408148, 3, 3, 3, 3)])
    print("*** Tested 'store_watch_data' Method ***")

    d_t, r_k, r_i, s_t, h_r = get_watch_data(999)
    print(d_t, r_k, r_i, s_t, h_r)
    print("*** Tested 'get_watch_data' Method ***")

    file_n = get_all_data()
    if os.path.isfile(file_n):
        print("*** Test 'get_all_data' Method ***")
    os.remove(file_n)
