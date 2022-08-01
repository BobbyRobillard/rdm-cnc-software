from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView, DeleteView, CreateView, UpdateView
from django.http import JsonResponse

from django.contrib import messages

from django.contrib.auth.models import User
from management.models import Setting, Lense
from management.forms import SettingForm, LenseForm
from django.forms import formset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import StandardBandit
from website.models import LenseInQueue

import csv, decimal

def update_diagnostics():
    try:
        lense = Setting.objects.get(pk=1).cnc_task.lense
        lense.amount_processed = lense.amount_processed + 1
        lense.save()
    except:
        pass

def cnc_is_locked():
    return Setting.objects.get(pk=1).cnc_is_locked

def cnc_is_busy():
    return not (Setting.objects.get(pk=1).cnc_task == None)

def read_csv(request):
    Lense.objects.all().delete()
    try:
        csv_file = request.FILES["csv_file"]

        if not csv_file.name.endswith('.csv'): # if wrong file type
            messages.error(request,'File is not CSV type')

        elif csv_file.multiple_chunks(): # if file is too large
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))

        else:
            file_data = csv_file.read().decode("utf-8")

            lines = file_data.split("\n")
            for line in lines:
                fields = line.split(",")
                try:
                    data = {
                        'make': fields[0],
                        'model': fields[1],
                        'diameter': fields[2],
                        'height': fields[3],
                        'type' : fields[4]
                    }
                    form = LenseForm(data) # Use our form to make sure csv data is valid

                    if form.is_valid():
                        form.save()
                    else:
                        messages.error(request, "Couldn't add: %s | %s | %s" % (fields[0], fields[1], fields[4]))
                except:
                    break

    except Exception as e:
        print(str(e))
    return True

def getInitialBandHeight(bandSize):
    return StandardBandit.objects.get(abbreviation=bandSize).initial_height

def getCutHeight(bandSize, diameter):
    cutHeight = 0

    if bandSize in "S" :
        if diameter >= 50 and diameter < 60:
            cutHeight = 1
        elif diameter >= 60 and diameter < 70:
            cutHeight = 2

    elif "M" in bandSize:
        if diameter >= 70 and diameter <= 80:
            cutHeight = 2
        elif diameter >= 81 and diameter <= 93:
            cutHeight = 4

    elif bandSize in "L":
        if diameter >= 94 and diameter <= 100:
            cutHeight = 2
        if diameter > 100 and diameter <= 110:
            cutHeight = 4
        elif diameter > 110:
            cutHeight = 5

    return cutHeight

def covert_negative_distances(distance):
    if distance <= 0:
        return 1
    return distance

def get_cnc_gcode():
    s = Setting.objects.get(pk=1)
    item = s.cnc_task

    if item is None:
        return ""

    # Created By: William Russetto
    step_pulse = 10
    step_idle_delay = 25
    step_port_invert = 0
    dir_port_invert = 1
    step_enable_invert = 0
    limit_pins_invert = 0
    probe_pin_invert = 0
    status_report = 31
    junction_deviation = 0.010
    arc_tolerance = 0.002
    report_inches = 0
    soft_limits_en = 1
    hard_limits_en = 1
    homing_dir_invert = 7
    homing_offset = 9.5
    homing_feed = 25
    homing_seek = 1500
    homing_debounce = 250
    homing_pull_off = 1
    lead_screw_pitch = 8
    steps_per_rev_x = 200
    steps_per_rev_y = 200
    steps_per_rev_z = 200
    microsteps_x = 8
    microsteps_y = 8
    microsteps_z = 8
    steps_per_mm_x = (steps_per_rev_x * microsteps_x) / lead_screw_pitch
    steps_per_mm_y = (steps_per_rev_y * microsteps_y) / lead_screw_pitch
    steps_per_mm_z = (steps_per_rev_z * microsteps_z) / lead_screw_pitch
    acceleration_x = 20
    acceleration_y = 20
    acceleration_z = 20
    max_travel_x = 200
    max_travel_y = 200
    max_travel_z = 200

    height = item.lense.height
    diameter = item.lense.diameter

    bandSize = item.lense.get_band_size()

    initial_band_height = getInitialBandHeight( str(bandSize) )

    cut_height = height + getCutHeight( str(bandSize), diameter )

    if cut_height < homing_offset:
        cut_height = homing_offset

    seek_rate_x = 4000
    seek_rate_y = 4000
    seek_rate_z = 6000
    feed_rate_z = 10
    x_distance = 0
    y_distance = 0
    total_distance_s = float(s.small_plunge_distance)
    total_distance_m = float(s.medium_plunge_distance)
    total_distance_l = float(s.large_plunge_distance)
    total_distance = 0
    feed_clearance = 5
    seek_distance = 0
    dwell_time = 5

    gcode_text = "$0 = " + str(step_pulse) + "\n"
    gcode_text += "$1 = " + str(step_idle_delay) + "\n"
    gcode_text += "$2 = " + str(step_port_invert) + "\n"
    gcode_text += "$3 = " + str(dir_port_invert) + "\n"
    gcode_text += "$4 = " + str(step_enable_invert) + "\n"
    gcode_text += "$5 = " + str(limit_pins_invert) + "\n"
    gcode_text += "$6 = " + str(probe_pin_invert) + "\n"
    gcode_text += "$10 = " + str(status_report) + "\n"
    gcode_text += "$11 = " + str(junction_deviation) + "\n"
    gcode_text += "$12 = " + str(arc_tolerance) + "\n"
    gcode_text += "$13 = " + str(report_inches) + "\n"
    gcode_text += "$20 = " + str(soft_limits_en) + "\n"
    gcode_text += "$21 = " + str(hard_limits_en) + "\n"
    gcode_text += "$22 = 1\n"
    gcode_text += "$23 = " + str(homing_dir_invert) + "\n"
    gcode_text += "$24 = " + str(homing_feed) + "\n"
    gcode_text += "$25 = " + str(homing_seek) + "\n"
    gcode_text += "$26 = " + str(homing_debounce) + "\n"
    gcode_text += "$27 = " + str(homing_pull_off) + "\n"
    gcode_text += "$100 = " + str(steps_per_mm_x) + "\n"
    gcode_text += "$101 = " + str(steps_per_mm_y) + "\n"
    gcode_text += "$102 = " + str(steps_per_mm_z) + "\n"
    gcode_text += "$110 = " + str(seek_rate_x) + "\n"
    gcode_text += "$111 = " + str(seek_rate_y) + "\n"
    gcode_text += "$112 = " + str(seek_rate_z) + "\n"
    gcode_text += "$120 = " + str(acceleration_x) + "\n"
    gcode_text += "$121 = " + str(acceleration_y) + "\n"
    gcode_text += "$122 = " + str(acceleration_z) + "\n"
    gcode_text += "$130 = " + str(max_travel_x) + "\n"
    gcode_text += "$131 = " + str(max_travel_y) + "\n"
    gcode_text += "$132 = " + str(max_travel_z) + "\n"

    if "S" in str(bandSize):
        total_distance = total_distance_s

    elif "M" in str(bandSize):
        total_distance = total_distance_m
    else:
        total_distance = total_distance_l

    x_distance = (initial_band_height - cut_height)/2
    y_distance = cut_height - decimal.Decimal(homing_offset)

    seek_distance = total_distance - feed_clearance

    gcode_text += "$H\n"
    gcode_text += "G10 P0 L20 X0 Y0 Z0\n"
    gcode_text += "G90\n"

    # Incase the band is super small, default to smallest size possible
    x_distance = covert_negative_distances(x_distance)
    y_distance = covert_negative_distances(y_distance)

    gcode_text += "G0 X" + str(x_distance) + "\n"
    gcode_text += "G0 Y" + str(y_distance) + "\n"
    gcode_text += "G0 Z" + str(seek_distance) + "\n"
    gcode_text += "G1 Z" + str(total_distance)  + " F" + str(feed_rate_z) + "\n"
    gcode_text += "G4 P" + str(dwell_time) + "\n"
    gcode_text += "$H" + "\n"

    return gcode_text
