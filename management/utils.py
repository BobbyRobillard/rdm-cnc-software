from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView

from management.models import Setting
from management.forms import SettingForm
