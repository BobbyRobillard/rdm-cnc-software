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

import csv

def update_setting(data):
    try:
        Setting.objects.update_or_create(pk=1,
            defaults = {
            "small_plunge_distance": data['small_plunge_distance'],
            "medium_plunge_distance": data['medium_plunge_distance'],
            "large_plunge_distance": data['large_plunge_distance'],
            "cnc_is_locked": data['cnc_is_locked'],
            "recent_orders_to_retain": data['recent_orders_to_retain'],
            }
        )
        return True
    except Exception as e:
        print(e)
        return False

def get_initial_setting():
    initial_setting, created = Setting.objects.get_or_create(pk=1, defaults={
        "small_plunge_distance": 0,
        "medium_plunge_distance": 0,
        "large_plunge_distance": 0,
        "cnc_is_locked": False,
        "recent_orders_to_retain": 0,
    })
    initial = {
        "small_plunge_distance": initial_setting.small_plunge_distance,
        "medium_plunge_distance": initial_setting.medium_plunge_distance,
        "large_plunge_distance": initial_setting.large_plunge_distance,
        "cnc_is_locked": initial_setting.cnc_is_locked,
        "recent_orders_to_retain": initial_setting.recent_orders_to_retain,
    }
    return initial

def read_csv(request):
    added = True
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
                except:
                    break

                form = LenseForm(data) # Use our form to make sure csv data is valid

                if not form.is_valid():
                    added = False
                else:
                    form.save()

    except Exception as e:
        print(str(e))
    return added
