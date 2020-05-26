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
from PIL import ImageFont  # Used for creating Data images


file_names = ["blank.png", "data.png", "plots.png", "test_file"]
testing = False


def create_start_image(s_image):
    """
    Method to create a blank plot area for application
    ARGS:       s_image - Byte stream of blank image
    Returns:    None
    """
    if testing:
        print("converting byte stream")
    with open(file_names[0], 'wb') as file:
        file.write(s_image)


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
    st_cum = [0]
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
    # Correct heart rate
    for i in range(1, len(h_r)):
        if h_r[i] > 220:
            h_r[i] = h_r[i-1]    
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
                r_k[i] == 49:
            walking += 1
        # Light Sleep
        elif r_k[i] == 112:
            if r_i[i] < 10:
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
        elif r_k[i] == 83 or r_k[i] == 115 or r_k[i] == 6:
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

    # Calculate Cumlative Step Count
    for i in range(1, len(s_t)):
        st_cum.append(st_cum[i-1] + s_t[i])
    if testing:
        print("creating plot")
    
    # Correct heart rate
    for i in range(1, len(h_r)):
        if h_r[i] > 220:
            h_r[i] = h_r[i-1]
    
    # Plot Data
    pylab.figure(figsize=(6.6, 6.6), dpi=60)
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

    create_start_image(image_file)
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
