from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from management.models import Lense

from .forms import QueueForm, SaveQueueForm

from .utils import add_to_queue

from .models import LenseInQueue, SavedQueue, SavedQueueItem

import json

@login_required
def homepage_view(request):
    context = {
    "form" : QueueForm(),
    "queue" : LenseInQueue.objects.filter(user=request.user),
    'save_form' : SaveQueueForm(),
    'saved_queues' : SavedQueue.objects.filter(user=request.user)
    }
    return render(request, "website/homepage.html", context)

@login_required
def change_model_view(request):
    make = request.GET['make']
    form = QueueForm()
    print("Make: " + make)
    form.fields['make'].initial = make

    models = Lense.objects.filter(make=make).values_list('model', flat=True).distinct()
    model_choices = [(model, model) for model in models]
    form.fields['model'].choices = model_choices
    context = {"form" : form}
    return JsonResponse({"new_form": render_to_string('website/queue_form.html', request=request, context=context)})

@login_required
def add_to_queue_view(request):
    if request.method == "POST":
        form = QueueForm(request.POST)

        if not form.is_valid():
            context = {
            "form" : form,
            "queue" : LenseInQueue.objects.filter(user=request.user)
            }
            return render(request, 'website/homepage.html', context)

        add_to_queue(request.user, form.cleaned_data)
    return redirect('website:homepage')

@login_required
def copy_item_view(request, pk):
    try:
        item = LenseInQueue.objects.get(pk=pk)
        LenseInQueue.objects.create(user=item.user, lense=item.lense)
    except:
        pass
    return redirect('website:homepage')

@login_required
def delete_from_queue_view(request, pk):
    try:
        item = LenseInQueue.objects.get(pk=pk)
        if request.user == item.user:
            item.delete()
    except:
        pass
    return redirect('website:homepage')

@login_required
def save_queue_view(request):
    if request.method == "POST":
        form = SaveQueueForm(request.POST)
        if form.is_valid():
            lenses_in_queue = LenseInQueue.objects.filter(user=request.user)
            sq = SavedQueue()
            sq.name = form.cleaned_data['name']
            sq.user = request.user
            sq.save()
            for item in lenses_in_queue:
                SavedQueueItem.objects.create(lense=item.lense, queue=sq)
            messages.success(request, "Queue saved!")
    return redirect('website:homepage')

@login_required
def add_bands_from_queue_view(request, pk):
    sq = SavedQueue.objects.get(pk=pk)
    for item in SavedQueueItem.objects.filter(queue=sq):
        LenseInQueue.objects.create(user=request.user, lense=item.lense)
    return redirect('website:homepage')

@login_required
def delete_saved_queue_view(request, pk):
    if SavedQueue.objects.filter(pk=pk, user=request.user).exists():
        SavedQueue.objects.get(pk=pk).delete()
    return redirect('website:homepage')
