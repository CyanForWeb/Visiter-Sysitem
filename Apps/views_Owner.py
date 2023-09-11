from django.shortcuts import render
from django.utils import timezone
from .models import *
from django.views.generic import ListView

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

#def videochat(request):
#    return render(request, 'html_Owner/VideoChat.html', )

def seeform(request):
    #db内容を日付順に並べ替える
    data_sort = Visitor_DB.objects.all().order_by('date','id').reverse()
    all_data = data_sort
    #htmlに渡したい値を格納
    context = {'object_list':all_data,}
    return render(request, 'html_Owner/Owner_seeform.html', context)

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
