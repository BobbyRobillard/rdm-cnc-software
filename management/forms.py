from django import forms
from management.utils import *

class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'

class LenseForm(forms.ModelForm):
    class Meta:
        model = Lense
        exclude = ('custom_band_size', )

class RoleForm(forms.Form):
    roles = (
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
    )
    user = forms.CharField(max_length=100)
    role = forms.ChoiceField(choices = roles)
