from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
import json

from reporting.utils import *
#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
class HomePageView(TemplateView):
    template_name = 'reporting/homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = {
            'diagnostics': Diagnostic.objects.all().order_by('amount_zoom_processed').order_by('amount_focus_processed')
        }
