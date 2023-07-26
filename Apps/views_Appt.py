from django.shortcuts import render
from django.utils import timezone
from .models import Post

def home(request):
    return render(request, 'html_Appt/Appt_home.html', )

def end(request):
    return render(request, 'html_Appt/Appt_end.html', )
