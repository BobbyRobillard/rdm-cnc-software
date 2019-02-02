from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from management.models import Setting, Lense
from management.forms import SettingForm, LenseForm


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
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("management:upload_csv"))
    #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("management:upload_csv"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
    #loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            data = {}
            data['zoom_height'] = fields[0]
            data['zoom_diameter'] = fields[1]
            data['focus_height'] = fields[2]
            data['focus_diameter'] = fields[3]
            data['make'] = fields[4]
            data['model'] = fields[5]
            try:
                form = LenseForm(data)
                if form.is_valid():
                    form.save()
            except Exception as e:
                return False

    except Exception as e:
        return False
    return True
