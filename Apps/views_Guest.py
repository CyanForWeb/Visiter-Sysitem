from django.shortcuts import render
from django.utils import timezone
from .models import *
from django.views.generic import TemplateView

#日時取得
from datetime import datetime

#iftttを使って送信する機能
import requests
import json

#カメラ機能
from django.http import JsonResponse
import base64
import json
from django.core.files.base import ContentFile


def home(request):
    return render(request, 'html_Guest/Guest_home.html', )


#-------その他　客人の画面で使用する機能たち---------------------------
def other(request):
    return render(request, 'html_Guest/Guest_other.html', )

def other_form(request): #質問フォーム1~3に移る際に使用
    if request.method == 'POST':
        #form1内容をdbに保存して、for2に遷移
        if "form1_submit" in request.POST: #ボタンが押されたら...
            form1 = request.POST.get('form1')
            Other_DB.objects.create(form1=form1) #Other_DBに値を保存
            Visitor_DB.objects.create(visitor='Other') #Visitor_DBに客人種類を保存
            #POSTリクエストを送信　質問フォーム１が送信されたら：住民に通知
            headers = {"Content-Type": "application/json"}
            cookies = {"test_cookie": "aaa"}
            data = json.dumps({"value1": "質問フォームが開始され、用件が入力されました！"})
            #住民のiftttのkeyを入力する↓
            requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
            return render(request, 'html_Guest/Guest_other_form2.html')
        #form2内容をdbに保存して、for3に遷移
        if "form2_submit" in request.POST: #ボタンが押されたら...
            form2_name = request.POST.get('form2_name')
            form2_address = request.POST.get('form2_address')
            form2_contact = request.POST.get('form2_contact')
            Other_DB.objects.update(form2_name=form2_name,
                                    form2_address=form2_address,
                                    form2_contact=form2_contact) #Other_DBに値を保存
            #POSTリクエストを送信　質問フォーム１が送信されたら：住民に通知
            headers = {"Content-Type": "application/json"}
            cookies = {"test_cookie": "aaa"}
            data = json.dumps({"value1": "名前、住所、連絡先が入力されました！"})
            #住民のiftttのkeyを入力する↓
            requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
            return render(request, 'html_Guest/Guest_other_form3.html')
    return render(request, 'html_Guest/Guest_other_form1.html')

def other_form4(request): #質問フォーム3→4に移る時に使う
    #form4に遷移したらform3のdbにmessage格納
    Other_DB.objects.update(form3 = "謎の動画閲覧終了")

    #POSTリクエストを送信　謎の動画の視聴が終わったら：住民に通知　ここの位置を確認する
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "aaa"}
    data = json.dumps({"value1": "謎の動画の視聴も終わりました！"})
    #住民のiftttのkeyを入力する↓
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)

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
            #POSTリクエストを送信　最後の質問も答えきったら：住民に通知
            headers = {"Content-Type": "application/json"}
            cookies = {"test_cookie": "aaa"}
            data = json.dumps({"value1": "お客さんは全ての質問の回答を終えました！"})
            #住民のiftttのkeyを入力する↓
            requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
            return render(request, 'html_Guest/Guest_other_end.html')
    return render(request, 'html_Guest/Guest_other_form4.html')


#-------配達員　の画面で使用する機能たち---------------------------
def delivery(request):
    return render(request, 'html_Guest/Guest_delivery.html', )

def delivery_camera(request):
    return render(request, 'html_Guest/Guest_delivery_camera.html', )

def delivery_end1(request):
    #POSTリクエストを送信　ハンコが必要な荷物がきたら：住民に通知
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "aaa"}
    data = json.dumps({"value1": "ハンコが必要な荷物です！今すぐ玄関へ！"})
    #住民のiftttのkeyを入力する↓
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
    return render(request, 'html_Guest/Guest_delivery_end1.html', )


#-------ポスト投函　の画面で使用する機能たち---------------------------
def post(request):
    return render(request, 'html_Guest/Guest_post.html', )

def post_end1(request):
    #POSTリクエストを送信　宛名認証をクリアしたら：住民に通知
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "aaa"}
    data = json.dumps({"value1": "宛名がある郵便物が投函されました！"})
    #住民のiftttのkeyを入力する↓
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
    return render(request, 'html_Guest/Guest_post_end1.html', )

def post_pic(request):
    return render(request, 'html_Guest/Guest_post_pic.html')

def post_end2(request):
    #POSTリクエストを送信　郵便物が撮影されたら：住民に通知
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "aaa"}
    data = json.dumps({"value1": "チラシが撮影されました！"})
    #住民のiftttのkeyを入力する↓
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
    return render(request, 'html_Guest/Guest_post_end2.html', )

#---------カメラ機能---------------
def save_snapshot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        snapshot_data = data.get('snapshotData', None)
        visitor_data = data.get('visitor', None)
        Visitor_DB.objects.create(visitor=visitor_data)#Visitor_DBに客人種類を保存
        if snapshot_data:
            # Base64形式のデータをデコードしてPost_DBに保存
            image_data = base64.b64decode(snapshot_data)
            #保存する際のファイル名を指定
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            #DBにimage_dataとvisitor情報を保存
            if visitor_data == 'Delivery':
                post_db = Delivery_DB()
                post_db.img.save(filename, ContentFile(image_data))
            else :
                post_db = Post_DB()
                post_db.visitor = visitor_data
                post_db.img.save(filename, ContentFile(image_data))
            return JsonResponse({'redirect': True})
    return JsonResponse({'message': 'スナップショットの保存に失敗しました。'}, status=400)
