from django.shortcuts import render
from django.utils import timezone
from .models import *

#iftttを使って送信する機能
import requests
import json


def home(request):
    return render(request, 'html_Guest/Guest_home.html', )


#-------その他　客人の画面で使用する機能たち---------------------------
def other(request):
    return render(request, 'html_Guest/Guest_other.html', )

def other_form1(request):
    #POSTリクエストを送信　STARTを押して質問フォーム１の画面になったら住民に通知
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "aaa"}
    data = json.dumps({"test": "hoge"})
    #住民のiftttのkeyを入力する↓
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)

    return render(request, 'html_Guest/Guest_other_form1.html', )

def other_form2(request):
    return render(request, 'html_Guest/Guest_other_form2.html', )

def other_form3(request):
    return render(request, 'html_Guest/Guest_other_form3.html', )

def other_form4(request):
    return render(request, 'html_Guest/Guest_other_form4.html', )

def other_end(request):
    return render(request, 'html_Guest/Guest_other_end.html', )


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
