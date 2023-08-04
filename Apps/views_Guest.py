from django.shortcuts import render
from django.utils import timezone
from .models import *
from django.views.generic import TemplateView

#iftttを使って送信する機能
import requests
import json


def home(request):
    return render(request, 'html_Guest/Guest_home.html', )


#-------その他　客人の画面で使用する機能たち---------------------------
def other(request):
    return render(request, 'html_Guest/Guest_other.html', )

def other_form(request):
    #POSTリクエストを送信　STARTを押して質問フォーム１の画面になったら住民に通知
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "aaa"}
    data = json.dumps({"test": "hoge"})
    #住民のiftttのkeyを入力する↓
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)

    if request.method == 'POST':
        #form1内容をdbに保存して、for2に遷移
        if "form1_submit" in request.POST: #ボタンが押されたら...
            form1 = request.POST.get('form1')
            Other_DB.objects.create(form1=form1) #Other_DBに値を保存
            return render(request, 'html_Guest/Guest_other_form2.html')
        #form2内容をdbに保存して、for3に遷移
        if "form2_submit" in request.POST: #ボタンが押されたら...
            form2_name = request.POST.get('form2_name')
            form2_address = request.POST.get('form2_address')
            form2_contact = request.POST.get('form2_contact')
            Other_DB.objects.update(form2_name=form2_name,
                                    form2_address=form2_address,
                                    form2_contact=form2_contact) #Other_DBに値を保存
            return render(request, 'html_Guest/Guest_other_form3.html')
    return render(request, 'html_Guest/Guest_other_form1.html')

def other_form4(request):
    #form4に遷移したらform3のdbにmessage格納
    Other_DB.objects.update(form3 = "謎の動画閲覧終了")
    if request.method == 'POST':
        #form4の内容をdbに保存して、endに遷移
        if "form4_submit" in request.POST: #ボタンが押されたら...
            form4_date = request.POST.get('form4_date')
            form4_day = request.POST.get('form4_day')
            form4_weather = request.POST.get('form4_weather')
            form4_transportation = request.POST.get('form4_transportation')
            form4_trivia = request.POST.get('form4_trivia')
            form4_message = request.POST.get('form4_message')
            Other_DB.objects.update(form4_date=form4_date,
                                    form4_day=form4_day,
                                    form4_weather=form4_weather,
                                    form4_transportation=form4_transportation,
                                    form4_trivia=form4_trivia,
                                    form4_message=form4_message) #Other_DBに値を保存
            return render(request, 'html_Guest/Guest_other_end.html')
    return render(request, 'html_Guest/Guest_other_form4.html')

#-------配達員　の画面で使用する機能たち---------------------------
def delivery(request):
    return render(request, 'html_Guest/Guest_delivery.html', )

def delivery_camera(request):
    return render(request, 'html_Guest/Guest_delivery_camera.html', )

def delivery_end1(request):
    #POSTリクエストを送信　STARTを押して質問フォーム１の画面になったら住民に通知
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "aaa"}
    data = json.dumps({"test": "hoge"})
    #住民のiftttのkeyを入力する↓
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
    return render(request, 'html_Guest/Guest_delivery_end1.html', )


#-------ポスト投函　の画面で使用する機能たち---------------------------
def post(request):
    return render(request, 'html_Guest/Guest_post.html', )

def post_end1(request):
    return render(request, 'html_Guest/Guest_post_end1.html', )

def post_pic(request):
    return render(request, 'html_Guest/Guest_post_pic.html', )

def post_end2(request):
    return render(request, 'html_Guest/Guest_post_end2.html', )
