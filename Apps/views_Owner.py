from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic
from datetime import datetime, date
from django.views.generic import ListView
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from .models import *
from .forms import Set_start, Set_finish

def home(request):
    data = Visitor_DB.objects.filter(date__date = date.today())
    #db内容を日付順に並べ替える
    data_sort = data.all().order_by('date','id').reverse()
    all_data = data_sort
    #htmlに渡したい値を格納
    record_status = 0
    if data.exists():
        record_status = 1
    context = {'object_list':all_data,'record_status':record_status}
    return render(request, 'html_Owner/Owner_home.html', context)

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
        return render(request, 'html_Owner/Owner_setting_end.html',)
    return render(request, 'html_Owner/Owner_setting_time.html', context)

def seeSettingTime(request):
    #db内容を日付順に並べ替える
    data_sort = Owner_Time_DB.objects.all().order_by('start_date')
    all_data = data_sort
    #htmlに渡したい値を格納
    context = {'object_list':all_data,}
    return render(request, 'html_Owner/Owner_seeSettingTime.html', context)

@require_POST
def deleteTime(request,id):
    data = Owner_Time_DB.objects.get(pk=id)
    data.delete()
    return redirect('Owner_seeSettingTime')

def setting_home(request):
    if "setHome_button" in request.POST:#ボタンが押されたら..
        return render(request, 'html_Owner/Owner_setting_end.html', )
    return render(request, 'html_Owner/Owner_setting_home.html', )

def setting_end(request):
    return render(request, 'html_Owner/Owner_setting_end.html', )

def seeform(request):
    #db内容を日付順に並べ替える
    data_sort = Visitor_DB.objects.all().order_by('date','id').reverse()
    all_data = data_sort
    #htmlに渡したい値を格納
    context = {'object_list':all_data,}
    return render(request, 'html_Owner/Owner_seeform.html', context)

@require_POST
def deleteForm(request,id):
    data_1 = Visitor_DB.objects.get(pk=id)
    date = data_1.date
    data_1.delete()
    if data_1.visitor=='Appt':
        data_2 = Appt_DB.objects.get(date=date)
    elif data_1.visitor=='Delivery':
        data_2 = Delivery_DB.objects.get(date=date)
    elif data_1.visitor=='Other':
        data_2 = Other_DB.objects.get(date=date)
    else:
        data_2 = Post_DB.objects.get(date=date)
    data_2.delete()
    return redirect('Owner_seeform')

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
            return render(request, 'html_Owner/Owner_home.html', )
        return render(request, 'html_Owner/Owner_seeform_detail_Appt.html', context)
    elif obj.visitor=='Delivery':
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
            return render(request, 'html_Owner/Owner_home.html', )
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
