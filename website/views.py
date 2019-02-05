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
    "makes" : Lense.objects.all().values_list('make', flat=True).distinct(),
    "models" : Lense.objects.all().values_list('model', flat=True).distinct(),
    "form" : QueueForm()
    }
    return render(request, "website/homepage.html", context)
