from django.shortcuts import render
from django.utils import timezone
from .models import *

def home(request):
    return render(request, 'html_Appt/Appt_home.html', )

def end(request):
    day_time = datetime.now() #今の日付時間を設定
    mes = Visitor_Message_DB.objects.get(visitor='Appt')
    Visitor_DB.objects.create(date=day_time,visitor='Appt',message=mes.message)#Visitor_DBに客人種類を保存
    Appt_DB.objects.create(date=day_time, visitor='Appt',video_status=0)#Appt_DBに保存
    return render(request, 'html_Appt/Appt_end.html', )
