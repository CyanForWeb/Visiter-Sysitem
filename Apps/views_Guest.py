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

#位置情報円
import matplotlib.pyplot as plt
import numpy as np


def home(request,number):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':number, 'true_number':true_number}
    return render(request, 'html_Guest/Guest_home.html', context)


#-------その他　客人の画面で使用する機能たち---------------------------
def other(request):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    return render(request, 'html_Guest/Guest_other.html', context)

def other_form(request): #質問フォーム1~3に移る際に使用
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    if request.method == 'POST':
        #form1内容をdbに保存して、for2に遷移
        if "form1_submit" in request.POST: #ボタンが押されたら...
            day_time = datetime.now() #今の日付時間を設定
            mes = Visitor_Message_DB.objects.get(visitor='Other')
            Visitor_DB.objects.create(date=day_time,visitor='Other',message=mes.message) #Visitor_DBに客人種類を保存
            form1 = request.POST.get('form1')
            Other_DB.objects.create(date=day_time, form1=form1) #Other_DBに値を保存
            #POSTリクエストを送信　質問フォーム１が送信されたら：住民に通知
            headers = {"Content-Type": "application/json"}
            cookies = {"test_cookie": "aaa"}
            data = json.dumps({"value1": "質問フォームが開始され、用件が入力されました！"})
            #住民のiftttのkeyを入力する↓
            #requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
            requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=data)
            return render(request, 'html_Guest/Guest_other_form2.html',context)
        #form2内容をdbに保存して、for3に遷移
        if "form2_submit" in request.POST: #ボタンが押されたら...
            form2_name = request.POST.get('form2_name')
            form2_contact = request.POST.get('form2_contact')
            Other_DB.objects.update(form2_name=form2_name,
                                    form2_contact=form2_contact) #Other_DBに値を保存
            #POSTリクエストを送信　質問フォーム2が送信されたら：住民に通知
            headers = {"Content-Type": "application/json"}
            cookies = {"test_cookie": "aaa"}
            data = json.dumps({"value1": "名前、住所、連絡先が入力されました！"})
            #住民のiftttのkeyを入力する↓
            #requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
            requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=data)
            return render(request, 'html_Guest/Guest_other_form3.html',context)
    return render(request, 'html_Guest/Guest_other_form1.html',context)

def other_form4(request): #質問フォーム3→4に移る時に使う
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    if request.method == 'GET':
        #form4に遷移したらform3のdbにmessage格納
        Other_DB.objects.update(form3 = "動画閲覧終了")

        #POSTリクエストを送信　謎の動画の視聴が終わったら：住民に通知　ここの位置を確認する
        headers = {"Content-Type": "application/json"}
        cookies = {"test_cookie": "aaa"}
        data = json.dumps({"value1": "謎の動画の視聴も終わりました！"})
        #住民のiftttのkeyを入力する↓
        #requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
        requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=data)
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
            #requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
            requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=data)
            return render(request, 'html_Guest/Guest_other_end.html',context)
    return render(request, 'html_Guest/Guest_other_form4.html',context)

def video(request):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    return render(request, 'html_Guest/video.html',context)

def other_check_video_status(request):
    if request.is_ajax():
        # レコードの最新のvideo_statusを取得
        latest_appt = Other_DB.objects.latest('pk')
        data = {
            'video_status': latest_appt.video_status,
        }
        return JsonResponse(data)


#-------配達員　の画面で使用する機能たち---------------------------
def delivery(request):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    if request.method == 'GET':
        time_status = 0
        if Owner_Time_DB.objects.filter(start_date__lte=datetime.now().date(),finish_date__gte=datetime.now().date()):
            time_status = 1
        context["time_status"]=time_status
    return render(request, 'html_Guest/Guest_delivery.html', context)

def delivery_drop(request):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "aaa"}
    data = json.dumps({"value1": "置き配されました！"})
    #住民のiftttのkeyを入力する↓
    #requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=data)
    return render(request, 'html_Guest/Guest_delivery_drop.html', context)

def delivery_camera(request):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    if request.method == 'GET':
        time_status = 0
        if Owner_Time_DB.objects.filter(start_date__lte=datetime.now().date(),finish_date__gte=datetime.now().date()):
            time_status = 1
        context["time_status"]=time_status
    return render(request, 'html_Guest/Guest_delivery_camera.html', context)

def delivery_end1(request):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    #POSTリクエストを送信　ハンコが必要な荷物がきたら：住民に通知
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "aaa"}
    data = json.dumps({"value1": "ハンコが必要な荷物です！今すぐ玄関へ！"})
    #住民のiftttのkeyを入力する↓
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=data)
    return render(request, 'html_Guest/Guest_delivery_end1.html', context)


#-------ポスト投函　の画面で使用する機能たち---------------------------
def post(request):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    return render(request, 'html_Guest/Guest_post.html', context)

def post_end1(request):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    #POSTリクエストを送信　宛名認証をクリアしたら：住民に通知
    #requests.post("https://maker.ifttt.com/trigger/post/with/key/bmJJC2vwlzldgPEhoZmrk3")
    requests.post("https://maker.ifttt.com/trigger/post/with/key/dPMcKW7OLMVpEKmN9HwjxZ")
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "aaa"}
    data = json.dumps({"value1": "宛名がある郵便物が投函されました！"})
    #住民のiftttのkeyを入力する↓
    #requests.post("https://maker.ifttt.com/trigger/post/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies)
    #requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=data)
    return render(request, 'html_Guest/Guest_post_end1.html', context)

def post_pic(request):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    return render(request, 'html_Guest/Guest_post_pic.html',context)

def post_end2(request):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    #POSTリクエストを送信　郵便物が撮影されたら：住民に通知
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "aaa"}
    data = json.dumps({"value1": "チラシが撮影されました！"})
    #住民のiftttのkeyを入力する↓
    #requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=data)
    return render(request, 'html_Guest/Guest_post_end2.html', context)


#---------カメラ撮影した画像をdbに保存する機能---------------
def save_snapshot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        snapshot_data = data.get('snapshotData', None)
        visitor_data = data.get('visitor', None)
        day_time = datetime.now() #今の日付時間を設定
        mes = Visitor_Message_DB.objects.get(visitor=visitor_data)
        Visitor_DB.objects.create(date=day_time, visitor=visitor_data,message=mes.message)#Visitor_DBに客人種類を保存
        if snapshot_data:
            # Base64形式のデータをデコードしてPost_DBに保存
            image_data = base64.b64decode(snapshot_data)
            #保存する際のファイル名を指定
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            #DBにimage_dataとvisitor情報を保存
            if visitor_data == 'Delivery': #客人がdeliveryだったら
                delivery_db = Delivery_DB()
                delivery_db.date = day_time
                delivery_db.visitor = "Delivery"
                delivery_db.img.save(filename, ContentFile(image_data))
            elif visitor_data == 'Drop': #客人がDropだったら
                delivery_db = Delivery_DB()
                delivery_db.date = day_time
                delivery_db.visitor = "Drop"
                delivery_db.img.save(filename, ContentFile(image_data))
            else : #客人がpostだったら
                post_db = Post_DB()
                post_db.visitor = visitor_data
                post_db.date = day_time
                post_db.img.save(filename, ContentFile(image_data))
            return JsonResponse({'redirect': True})
    return JsonResponse({'message': 'スナップショットの保存に失敗しました。'}, status=400)


#---------geolocationの範囲設定---------------
def save_geolocations(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)

        true_number = Owner_DB.objects.get(owner='Owner')
        data_1 = true_number.location
        Owner_data = json.loads(data_1)
        Owner_latitude = Owner_data.get('latitude', None)
        Owner_longitude = Owner_data.get('longitude', None)

<<<<<<< HEAD

=======
>>>>>>> 7c7c4e0 (Risa 12/2)
        #if latitude - 0.00045 <= Owner_latitude < latitude + 0.00045 and longitude - 0.0005 <= Owner_longitude < longitude + 0.0005:        #console.log("a")
        num = 0.0005**2 + 0.00045**2
        r = ((latitude-Owner_latitude)**2 + (longitude-Owner_longitude)**2)
        if r <= num:
<<<<<<< HEAD
=======

        #if latitude - 0.00045 <= Owner_latitude < latitude + 0.00045 and longitude - 0.0005 <= Owner_longitude < longitude + 0.0005:
>>>>>>> 7c7c4e0 (Risa 12/2)

        #num = 0.0005**2 + 0.00045**2
        #r = ((latitude-Owner_latitude)**2 + (longitude-Owner_longitude)**2)
        #if r <= num:
        #if latitude - 0.0005 <= Owner_latitude < latitude + 0.0005 and longitude - 0.00005 <= Owner_longitude < longitude + 0.00005:
            #デバックの時に使う
            #保存する際のファイル名を指定
            #filename = f"OK_GEO_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            #f = open('media/post/'+filename, "w")
            #f.write("request.body:")
            #f.write(json.dumps(data))
            #f.write("Owner_data:")
            #f.write(json.dumps(Owner_data))
            #f.close()

            #requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=payload)
<<<<<<< HEAD

=======
>>>>>>> 7c7c4e0 (Risa 12/2)
            return JsonResponse({'redirect': True})

        else:

            #デバックの時に使う
            #保存する際のファイル名を指定
            #filename = f"NG_GEO_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            #f = open('media/post/'+filename, "w")
            #f.write("request.body:")
            #f.write(json.dumps(data))
            #f.write("Owner_data:")
            #f.write(json.dumps(Owner_data))
            #f.close()
            return JsonResponse({'redirect': False,'message':'<br>位置情報が正しくありません。<br>QRコードに近づいて再度読み込んでください。'})
    return JsonResponse({'message': '位置情報が取得できませんでした。'}, status=400)
