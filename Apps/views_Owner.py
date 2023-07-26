from django.shortcuts import render
from django.utils import timezone
from .models import Post

def home(request):
    return render(request, 'html_Owner/Owner_home.html', )

def setting(request):
    return render(request, 'html_Owner/Owner_setting.html', )

def seeform(request):
    return render(request, 'html_Owner/Owner_seeform.html', )
