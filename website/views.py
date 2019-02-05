from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from management.models import Lense

from .forms import QueueForm

import json

@login_required
def homepage_view(request):
    context = {
    "form" : QueueForm()
    }
    return render(request, "website/homepage.html", context)

def add_to_queue_view(request):
    if request.method == "POST":
        form = QueueForm(request.POST)

        if not form.is_valid():
            return render(request, 'website/homepage.html', {"form" : form})

        add_to_queue(request.user, form.cleaned_data)
    return redirect('website:homepage')
