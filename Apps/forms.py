from django import forms
from .models import *
from django.http import HttpResponse

from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget

class Set_start(forms.ModelForm):
    class Meta:
        model = Owner_Time_DB
        fields = ('start_date', 'start_time',)
        widgets = {
            'start_date': forms.NumberInput(attrs={"type": "date"}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class Set_finish(forms.ModelForm):
    class Meta:
        model = Owner_Time_DB
        fields = ('finish_date', 'finish_time',)
        widgets = {
            'finish_date': forms.NumberInput(attrs={"type": "date"}),
            'finish_time': forms.TimeInput(attrs={'type': 'time'}),
        }
