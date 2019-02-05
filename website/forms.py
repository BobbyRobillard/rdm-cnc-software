from django import forms

from management.models import Lense

class QueueForm(forms.Form):

    type_choices = (
        ("zoom", "zoom"),
        ("focus", "focus"),
    )

    make = forms.ChoiceField(choices=Lense.objects.all().values_list('make', flat=True).distinct())
    model = forms.ChoiceField(choices=Lense.objects.all().values_list('model', flat=True).distinct())
    type = forms.ChoiceField(choices=type_choices)
    custom_size = forms.CharField(max_length=25)
    save_as_default = forms.BooleanField()
