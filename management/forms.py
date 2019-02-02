from django import forms
from management.utils import *

class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'
