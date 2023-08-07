from django.shortcuts import render
from django.utils import timezone
from .models import *

def home(request):
    return render(request, 'html_Appt/Appt_home.html', )

def end(request):
    Visitor_DB.objects.create(visitor='Appt')#Visitor_DBに客人種類を保存
    Appt_DB.objects.create(visitor='Appt',video_status=0)#Appt_DBに保存
    return render(request, 'html_Appt/Appt_end.html', )
