#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  image.py
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

import time
import d_base
import os  # Used for testing and cleanup
import pylab  # Used for plotting data
from PIL import Image  # Used for creating Data images
from PIL import ImageDraw  # Used for creating Data images
#from PIL import ImageFont  # Used for creating Data images
#import pyecharts


file_names = ["blank.png", "icon.svg", "data.png", "plots.png", "test_file"]
testing = False


def create_start_images(s_image, a_icon):
    """
    Method to create a blank plot area for application
    ARGS:       s_image - Byte stream of blank image
    Returns:    None
    """
    if testing:
        print("converting byte stream")
    with open(file_names[0], 'wb') as file:
        file.write(s_image)
    with open(file_names[1], 'wb') as file:
        file.write(a_icon)


def create_data_image(hours):
    """
    Method to create image with written word for the number of hours provided
    ARGS:       hours - number of hours to retreive from database
    RETURNS:    None
    """
    if testing:
        print("creating data image")
    else:
        clean_up()
    # Get Database Data
    d_t, r_k, r_i, s_t, h_r = d_base.get_watch_data(hours)
    total_st = 0
    total_hr = 0
    running = 0
    walking = 0
    sleep_l = 0
    sleep_h = 0
    sitting = 0
    not_worn = 0
    unknown = 0
    sedentary = 0
    hs_count = 0
    denominator = round((hours/24), 2)

    # Step Calculations
    tot_st = sum(s_t)
    aver_st = round(tot_st/len(s_t), 2)
    step_h = round(tot_st/hours, 2)

    h_r = cleanse_hr(h_r)

    # Heart Rate Calculations
    tot_hr = sum(h_r)
    aver_hr = round(tot_hr/len(h_r), 2)

    # Activity Type Calculation
    for i in range(len(d_t)):
        # Running
        if r_k[i] == 98 or \
            r_k[i] == 66 or \
            r_k[i] == 50 or \
                r_k[i] == 82:
            running += 1
        # Walking
        elif r_k[i] == 1 or \
            r_k[i] == 16 or \
            r_k[i] == 17 or \
            r_k[i] == 33 or \
            r_k[i] == 18 or \
            r_k[i] == 34 or \
            r_k[i] == 65 or \
                r_k[i] == 49:
            walking += 1
        # Light Sleep
        elif r_k[i] == 112:
            if r_i[i] <= 12:
                hs_count += 1
                if hs_count >= 20:
                    sleep_h += 1
                else:
                    sleep_l += 1
            else:
                hs_count = 0
                sleep_l += 1
        # Heavy sleep
        elif r_k[i] == 122:
            sleep_h += 1
        # Sitting
        elif r_k[i] == 80 or r_k[i] == 96 or r_k[i] == 99:
            sitting += 1
        # Not worn right way up, Not worn right way down or Charging
        elif r_k[i] == 83 or \
            r_k[i] == 115 or \
            r_k[i] == 6 or \
                r_k[i] == 3:
            not_worn += 1
        # sitting for 5 minutes straight
        elif r_k[i] == 90:
            sedentary += 5
        # Unknown Activities
        else:
            unknown += 1

    sle_la = round(sleep_l/denominator, 2)
    sle_ha = round(sleep_h/denominator, 2)
    sleepa = round((sleep_l+sleep_h)/denominator, 2)
    walk_a = round(walking/denominator, 2)
    runn_a = round(running/denominator, 2)

    image_header = "Data Analysis for last {} Hours\n".format(hours)
    image_head_s = "***** Step Data  ******\n"
    image_step_t = "Total Steps Taken     :{}\n".format(tot_st)
    image_step_h = "Hourly Step Average   :{}\n".format(step_h)
    image_step_a = "Minute Step Average   :{}\n".format(aver_st)
    image_head_h = "***** Heart Rate ******\n"
    image_hear_t = "Total Heart Beats     :{}\n".format(tot_hr)
    image_hear_a = "Heart Beat Average    :{}\n".format(aver_hr)
    image_head_r = "**** Sleeping Data ****\n"
    image_sle_li = "Light Sleep Minutes   :{}\n".format(sleep_l)
    image_sle_la = "Light Sleep Average   :{}\n".format(sle_la)
    image_sle_he = "Heavy Sleep Minutes   :{}\n".format(sleep_h)
    image_sle_ha = "Heavy Sleep Average   :{}\n".format(sle_ha)
    image_sleepa = "Average Sleep         :{}\n".format(sleepa)
    image_head_a = "***** Activities *****\n"
    image_sittin = "Sitting Time          :{}\n".format(sitting)
    image_sedent = "Sedentary Time        :{}\n".format(sedentary)
    image_walk_t = "Walking Time          :{}\n".format(walking)
    image_walk_a = "Walking Time Average  :{}\n".format(walk_a)
    image_runn_t = "Running Time          :{}\n".format(running)
    image_runn_a = "Running Time Average  :{}\n".format(runn_a)
    image_not_wo = "Bip Not Worn          :{}\n".format(not_worn)

    image_input = " ".join(
        (image_header, image_head_s, image_step_t,
            image_step_h, image_step_a, image_head_h, image_hear_t,
            image_hear_a, image_head_r, image_sle_li, image_sle_la,
            image_sle_he, image_sle_ha, image_sleepa, image_head_a,
            image_sittin, image_sedent, image_walk_t, image_walk_a,
            image_runn_t, image_runn_a, image_not_wo))

    image_base = Image.new('RGB', (355, 355), color='white')
    data_image = ImageDraw.Draw(image_base)
    data_image.multiline_text((2, 2), image_input, fill=(0, 0, 0))
    image_base.save("data.png")


def create_plot_image(hours):
    if testing:
        print("creating plot image method started")
    else:
        clean_up()
    # Get Database Data
    d_t, r_k, r_i, s_t, h_r = d_base.get_watch_data(hours)

    st_cum = [0]
    for i in range(1, len(s_t)):
        st_cum.append(st_cum[i-1] + s_t[i])

    h_r = cleanse_hr(h_r)

    if testing:
        print("creating plot")

    # Plot Data
    pylab.figure(figsize=(6.4, 6.4), dpi=60)
    pylab.subplot(311)
    pylab.plot(s_t, '-g')
    pylab.ylabel("Steps")
    pylab.gca().set_xticklabels([])
    pylab.title("Plots for Last {} Hours".format(hours))
    pylab.subplot(312)
    pylab.plot(h_r, '-r')
    pylab.ylabel("Heart Rate")
    pylab.gca().set_xticklabels([])
    pylab.subplot(313)
    pylab.plot(st_cum, '-b')
    pylab.ylabel("Total Steps")
    pylab.gca().set_xticklabels([])
    if testing:
        print("About to save Plot")
    pylab.savefig("plots.png", bbox_inches='tight')

"""
def create_plot_image(hours)
    if testing:
        print("creating plot image method started")
    else:
        clean_up()
    # Get Database Data
    d_t, r_k, r_i, s_t, h_r = d_base.get_watch_data(hours)

    st_cum = [0]
    for i in range(1, len(s_t)):
        st_cum.append(st_cum[i-1] + s_t[i])

    h_r = cleanse_hr(h_r)

    if testing:
        print("creating plot")
"""


def cleanse_hr(h_r):
    if testing:
        print("HR data being cleansed")

    # Correct heart rate by removing values greater than 220
    for i in range(1, len(h_r)):
        if h_r[i] > 220:
            h_r[i] = h_r[i-1]

    return h_r


def clean_up():
    """
    method for deleting files when needed
    ARGS:       None
    RETURNS:    None
    """
    if testing:
        print("Deleting all Files")
    for i in range(len(file_names)):
        if os.path.isfile(file_names[i]):
            os.remove(file_names[i])


if testing:
    """
    Testing for all methods in this program
    """

    image_file = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01h\x00\x00\x01h\x08\x02\x00\x00\x00\xf5\x87\xf6\x82\x00\x00\x00\tpHYs\x00\x00\t:\x00\x00\t:\x01\xf0d\x92J\x00\x00\x00\x18tEXtComment\x00Andrew Taylor(c)(\x89I\xeb\x00\x00\x03ZIDATx\xda\xed\xd41\x01\x00\x00\x08\xc30\xc0\x0f\xc7\xfc\x9bC\x03\x7f"\xa1G;\x9b\x02\xf8\x18\t\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8cC\x02\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x000\x0e\xc08\x00\xe3\x00\x8c\x030\x0e\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\x8c\x030\x0e\xc08\x00\xe3\x00\x8c\x03\xc08\x00\xe3\x00\x8c\x030\x0e\xc08\x00\xe3\x00\xf89}\x01\x03_\xb7\x12c \x00\x00\x00\x00IEND\xaeB`\x82'
    icon_file = b'<?xml version="1.0" encoding="UTF-8"?>\n<!-- Created with Inkscape (http://www.inkscape.org/) -->\n<svg width="192" height="192" version="1.1" viewBox="0 0 192 192" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:cc="http://creativecommons.org/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><metadata><rdf:RDF><cc:Work rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"/><dc:title/></cc:Work></rdf:RDF></metadata><defs><clipPath id="clipPath16"><path d="m0 192h192v-192h-192v192z"/></clipPath><clipPath id="clipPath26"><path d="m-4.883e-4 192h192v-192h-192v192z"/></clipPath><clipPath id="clipPath34"><path d="m-4.883e-4 192h192v-192h-192v192z"/></clipPath><clipPath id="clipPath38"><path d="m0 192h192v-192h-192v192z"/></clipPath><clipPath id="clipPath42"><path d="m0 192h192v-192h-192v192z"/></clipPath><clipPath id="clipPath116"><path d="m0 192h192v-192h-192v192z"/></clipPath><clipPath id="clipPath120"><path d="m0 192h192v-192h-192v192z"/></clipPath><clipPath id="clipPath124"><path d="m192 192h-192v-192h192v192z"/></clipPath></defs><g transform="matrix(1.25,0,0,-1.25,0,192)"><g transform="scale(.8)" fill="#666" fill-opacity=".7992"><g clip-path="url(#clipPath16)" fill="#666" fill-opacity=".7992"><g transform="matrix(1,0,0,-1,0,192)"><g fill="#666" fill-opacity=".7992"><g clip-path="url(#clipPath26)" fill="#666" fill-opacity=".7992"><g fill="#666" fill-opacity=".7992"><g fill="#666" fill-opacity=".7992"><g clip-path="url(#clipPath34)" fill="#666" fill-opacity=".7992" opacity=".4"><g clip-path="url(#clipPath38)" fill="#666" fill-opacity=".7992"><g transform="translate(.2497 .2497)" fill="#666" fill-opacity=".7992"><path d="m0 0 191.5 191.5" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g></g><path d="m0 0h192v192h-192zm0.249 191.8h191.5v-191.5h-191.5z"/><g clip-path="url(#clipPath42)" fill="#666" fill-opacity=".7992"><g transform="translate(191.7 .2497)"><path d="m0 0-191.5 191.5" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(124 -4e-4)"><path d="m0 0v192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(68 -4e-4)"><path d="m0 0v192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(192 124)"><path d="m0 0h-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(192 68)"><path d="m0 0h-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(136 96)"><path d="m0 0c0 22.09-17.91 40-40 40s-40-17.91-40-40 17.91-40 40-40 40 17.91 40 40z" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(-4e-4 96)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(96 -5e-4)"><path d="m0 0v192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(96 8)"><path d="m0 0c-48.6 0-88 39.4-88 88s39.4 88 88 88 88-39.4 88-88-39.4-88-88-88m0 0.25c48.39 0 87.75 39.36 87.75 87.75s-39.36 87.75-87.75 87.75-87.75-39.36-87.75-87.75 39.36-87.75 87.75-87.75" fill="#666" fill-opacity=".7992"/></g><g transform="translate(160 20)"><path d="m0 0h-128c-6.6 0-12 5.4-12 12v128c0 6.6 5.4 12 12 12h128c6.6 0 12-5.4 12-12v-128c0-6.6-5.4-12-12-12m0 0.25c6.479 0 11.75 5.271 11.75 11.75v128c0 6.479-5.271 11.75-11.75 11.75h-128c-6.479 0-11.75-5.271-11.75-11.75v-128c0-6.479 5.271-11.75 11.75-11.75h128" fill="#666" fill-opacity=".7992"/></g><g transform="translate(148 8)"><path d="m0 0h-104c-6.6 0-12 5.4-12 12v152c0 6.6 5.4 12 12 12h104c6.6 0 12-5.4 12-12v-152c0-6.6-5.4-12-12-12m0 0.25c6.479 0 11.75 5.271 11.75 11.75v152c0 6.479-5.271 11.75-11.75 11.75h-104c-6.479 0-11.75-5.271-11.75-11.75v-152c0-6.479 5.271-11.75 11.75-11.75h104" fill="#666" fill-opacity=".7992"/></g><g transform="translate(172 32)"><path d="m0 0h-152c-6.6 0-12 5.4-12 12v104c0 6.6 5.4 12 12 12h152c6.6 0 12-5.4 12-12v-104c0-6.6-5.4-12-12-12m0 0.25c6.479 0 11.75 5.271 11.75 11.75v104c0 6.479-5.271 11.75-11.75 11.75h-152c-6.479 0-11.75-5.271-11.75-11.75v-104c0-6.479 5.271-11.75 11.75-11.75h152" fill="#666" fill-opacity=".7992"/></g></g></g></g></g></g></g></g><g fill="#666" fill-opacity=".7992"><g clip-path="url(#clipPath116)" fill="#666" fill-opacity=".7992" opacity=".15"><g transform="matrix(1,0,0,-1,0,192)" fill="#666" fill-opacity=".7992"><g fill="#666" fill-opacity=".7992"><g clip-path="url(#clipPath120)" fill="#666" fill-opacity=".7992"><g clip-path="url(#clipPath124)" fill="#666" fill-opacity=".7992"><g transform="translate(4 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(8 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(12 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(16 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(20 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(24 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(28 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(32 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(36 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(40 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(44 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(48 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(52 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(56 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(60 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(64 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(68 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(72 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(76 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(80 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(84 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(88 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(92 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(96 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(100 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(104 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(108 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(112 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(116 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(120 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(124 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(128 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(132 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(136 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(140 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(144 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(148 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(152 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(156 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(160 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(164 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(168 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(172 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(176 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(180 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(184 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(188 192)"><path d="m0 0v-192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 4)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 8)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 12)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 16)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 20)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 24)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 28)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 32)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 36)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 40)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 44)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 48)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 52)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 56)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 60)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 64)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 68)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 72)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 76)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 80)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 84)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 88)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 92)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 96)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 100)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 104)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 108)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 112)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 116)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 120)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 124)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 128)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 132)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 136)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 140)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 144)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 148)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 152)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 156)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 160)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 164)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 168)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 172)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 176)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 180)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 184)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g><g transform="translate(0 188)"><path d="m0 0h192" fill="#666" fill-opacity=".7992" stroke="#000" stroke-miterlimit="10" stroke-width=".25"/></g></g><path d="m0 1e-3h192v192h-192zm0.25 191.7h191.5v-191.5h-191.5z"/></g></g></g></g></g></g></g></g><g><rect x="28.37" y="12.41" width="135.3" height="167.5" ry="8.225" fill-opacity=".8543" stroke="#000" stroke-linecap="round" stroke-linejoin="round" stroke-width="8.482"/><text x="35.333336" y="119.33334" fill="#ffffff" font-family="Sans" font-size="13.33px" letter-spacing="0px" stroke="#ffffff" stroke-width="1px" word-spacing="0px" style="line-height:125%" xml:space="preserve"><tspan x="35.333336" y="119.33334" fill="#ffffff" font-family="\'hooge 05_53\'" font-size="74.67px" stroke="#ffffff" stroke-width="1px" style="font-feature-settings:normal;font-variant-caps:normal;font-variant-ligatures:normal;font-variant-numeric:normal">BIP</tspan></text><g stroke="#000" stroke-linecap="round" stroke-linejoin="round">\n<rect x="47.08" y=".4557" width="9.422" height="7.749"/><rect x="135.3" y=".25" width="9.422" height="7.749"/><rect x="135.3" y="184" width="9.422" height="7.749"/><rect x="47.29" y="184" width="9.422" height="7.749"/></g><path d="m175.7 96a4 14 0 0 1-3.97 14 4 14 0 0 1-4.029-13.79 4 14 0 0 1 3.911-14.2 4 14 0 0 1 4.087 13.58l-3.998 0.4147z" fill="#0f0000" stroke="#000" stroke-linecap="round" stroke-linejoin="round"/></g></svg>\n'
    create_start_images(image_file, icon_file)
    if os.path.isfile(file_names[0]):
        os.remove(file_names[0])
        print("*** Tested 'create_start_image' successfully ***")
    else:
        print("Failed 'create_start_image'")

    create_data_image(100)
    if os.path.isfile(file_names[1]):
        os.remove(file_names[1])
        print("*** Tested 'create_data_image' successfully ***")
    else:
        print("Failed 'create_data_image'")

    create_plot_image(100)
    if os.path.isfile(file_names[2]):
        os.remove(file_names[2])
        print("*** Tested 'create_plot_image' successfully ***")
    else:
        print("Failed 'create_plot_image'")

    os.mknod(file_names[3])
    clean_up()
    if not os.path.isfile(file_names[3]):
        print("*** Tested 'clean_up' successfully")
    else:
        print("Failed 'clean_up'")
