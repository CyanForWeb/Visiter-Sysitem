from django.shortcuts import render
from django.utils import timezone
from .models import *

def home(request):
    return render(request, 'html_Owner/Owner_home.html', )

def setting(request):
    return render(request, 'html_Owner/Owner_setting.html', )

def setting_time(request):
    return render(request, 'html_Owner/Owner_setting_time.html', )

def setting_home(request):
    return render(request, 'html_Owner/Owner_setting_home.html', )

def setting_end(request):
    return render(request, 'html_Owner/Owner_setting_end.html', )

def seeform(request):
    return render(request, 'html_Owner/Owner_seeform.html', )

def seeform_detail(request):
    return render(request, 'html_Owner/Owner_seeform_detail.html', )
