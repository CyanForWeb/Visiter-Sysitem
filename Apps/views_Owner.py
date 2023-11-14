from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic
from datetime import datetime, date
from django.views.generic import ListView
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from PIL import Image
import qrcode
import base64
from io import BytesIO
import random
from random import randrange

from .models import *
from .forms import Set_start, Set_finish

def home(request):
    if Owner_DB.objects.all().count()==0:
        Owner_DB.objects.create()
    data = Visitor_DB.objects.filter(date__date = date.today())
    #db内容を日付順に並べ替える
    today_data_sort = data.all().order_by('date','id').reverse()
    today_data = today_data_sort
    #htmlに渡したい値を格納
    record_status = 0
    if data.exists(): #今日の来客者がいるか確認
        record_status = 1
    #全ての来客者履歴
    #db内容を日付順に並べ替える
    all_data_sort = Visitor_DB.objects.all().order_by('date','id').reverse()
    all_data = all_data_sort
    #htmlに渡したい値を格納
    context = {'today_list':today_data,'record_status':record_status, 'all_list':all_data}
    return render(request, 'html_Owner/Owner_home.html', context)

import time
def setting_time(request):
    context = {
               'set_start':Set_start(),
               'set_finish':Set_finish(),
               }
    if "setTime_button" in request.POST:#ボタンが押されたら..
        start = Set_start(request.POST)
        if not start.is_valid():
             return HttpResponse('start', status=500)
        finish = Set_finish(request.POST)
        if not finish.is_valid():
             return HttpResponse('finish', status=500)
        start_date  = start.cleaned_data['start_date']
        start_time  = start.cleaned_data['start_time']
        finish_date  = finish.cleaned_data['finish_date']
        finish_time  = finish.cleaned_data['finish_time']
        Owner_Time_DB.objects.create(start_date=start_date,
                                     start_time=start_time,
                                     finish_date=finish_date,
                                     finish_time=finish_time)
        time.sleep(3)
        return redirect('Owner_seeSettingTime')
    return render(request, 'html_Owner/Owner_setting_time.html', context)

def seeSettingTime(request):
    #古い履歴を消す
    old_data = Owner_Time_DB.objects.filter(finish_date__lte=datetime.now().date())
    old_data.delete()
    #db内容を日付順に並べ替える
    data_sort = Owner_Time_DB.objects.all().order_by('start_date')
    all_data = data_sort
    record_status = 0
    if all_data.exists():
        record_status = 1
    #htmlに渡したい値を格納
    context = {'object_list':all_data, 'record_status':record_status}
    return render(request, 'html_Owner/Owner_seeSettingTime.html', context)

@require_POST
def deleteTime(request,id):
    data = Owner_Time_DB.objects.get(pk=id)
    data.delete()
    return redirect('Owner_seeSettingTime')

def setting_home(request):
    return render(request, 'html_Owner/Owner_setting_home.html', )

def setting_end(request):
    return render(request, 'html_Owner/Owner_setting_end.html', )

def guest(request):
    context = {}
    newText = Owner_DB.objects.get(owner='Owner')
    context['newText'] = newText
    if request.method == 'POST':
        url = request.POST['url']
        img = qrcode.make(url)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
        context['qr'] = qr
    return render(request, 'html_Owner/Owner_guest.html', context)

def guest_security(request):
    if request.method == 'POST':
        newText = randrange(100000)
        Owner_DB.objects.update(update_url_text=newText)
        return redirect('Owner_home')
    return render(request, 'html_Owner/Owner_guest_security.html')

@require_POST
def deleteForm(request,id):
    data_1 = Visitor_DB.objects.get(pk=id)
    date = data_1.date
    data_1.delete()
    if data_1.visitor=='Appt':
        data_2 = Appt_DB.objects.get(date=date)
    elif data_1.visitor=='Delivery' or data_1.visitor=='Drop':
        data_2 = Delivery_DB.objects.get(date=date)
    elif data_1.visitor=='Other':
        data_2 = Other_DB.objects.get(date=date)
    else:
        data_2 = Post_DB.objects.get(date=date)
    data_2.delete()
    return redirect('Owner_home')

def seeform_detail(request, id):
    obj = Visitor_DB.objects.get(pk=id)
    context = {}

    if obj.visitor=='Appt':
        visit = appt_context(request,obj)
        context = {'obj':visit,'mes':obj,}
        if "video_button" in request.POST:#ボタンが押されたら...
            visit.video_status = 1
            visit.save()
            return render(request, 'html_Owner/VideoChat.html',)
        if "exit_button" in request.POST:#ボタンが押されたら...
            visit.video_status = 0
            visit.save()
            return redirect('Owner_home')
        return render(request, 'html_Owner/Owner_seeform_detail_Appt.html', context)
    elif obj.visitor=='Delivery' or obj.visitor=='Drop':
        visit = delivery_context(obj)
        context = {'obj':visit,'mes':obj,}
        return render(request, 'html_Owner/Owner_seeform_detail.html', context)
    elif obj.visitor=='Other':
        visit = other_context(request,obj)
        context = {'obj':visit,'mes':obj,}
        if "video_button" in request.POST:#ボタンが押されたら...
            visit.video_status = 1
            visit.save()
            return render(request, 'html_Owner/VideoChat.html',)
        if "exit_button" in request.POST:#ボタンが押されたら...
            visit.video_status = 0
            visit.save()
            return redirect('Owner_home')
        return render(request, 'html_Owner/Owner_seeform_detail_Other.html', context)
    else:
        visit = post_context(obj)
        context = {'obj':visit,'mes':obj,}
        return render(request, 'html_Owner/Owner_seeform_detail.html', context)


#visitorの種類ごとにcontextの内容を格納する
def appt_context(request,obj):
    visit = Appt_DB.objects.get(date=obj.date)
    return visit
#visitorの種類ごとにcontextの内容を格納する
def delivery_context(obj):
    visit = Delivery_DB.objects.get(date=obj.date)
    return visit
#visitorの種類ごとにcontextの内容を格納する
def other_context(request,obj):
    visit = Other_DB.objects.get(date=obj.date)
    return visit
#visitorの種類ごとにcontextの内容を格納する
def post_context(obj):
    visit = Post_DB.objects.get(date=obj.date)
    return visit

#位置情報
import requests
import json
from django.http import JsonResponse
import base64
from django.core.files.base import ContentFile

def save_geolocation_Owner_setting(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)
        payload = json.dumps({"latitude": latitude,"longitude": longitude})
        Owner_DB.objects.update(location=payload)
        return JsonResponse({'redirect': True})
    return JsonResponse({'message': '位置情報が取得できませんでした。'}, status=400)
