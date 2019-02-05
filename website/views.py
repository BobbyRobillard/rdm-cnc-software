from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from management.models import Lense

import json

@login_required
def homepage_view(request):
    context = {
    "makes" : Lense.objects.all().values_list('make', flat=True).distinct(),
    }
    return render(request, "website/homepage.html", context)
