from django import forms
from management.utils import *

class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'

class LenseForm(forms.ModelForm):
    class Meta:
        model = Lense
        exclude = ('custom_band_size', 'amount_processed')
