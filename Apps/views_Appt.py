from django.shortcuts import render, redirect
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

def home(request,number):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':number,'true_number':true_number}
    return render(request, 'html_Appt/Appt_home.html', context)

def end(request):
    day_time = datetime.now() #今の日付時間を設定
    mes = Visitor_Message_DB.objects.get(visitor='Appt')
    Visitor_DB.objects.create(date=day_time,visitor='Appt',message=mes.message)#Visitor_DBに客人種類を保存
    Appt_DB.objects.create(date=day_time, visitor='Appt',video_status=0)#Appt_DBに保存
    #住民のiftttのkeyを入力する↓
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "qrcode"}
    payload = json.dumps({"value1": "アポ済みのお客さんが到着しました！今すぐ玄関へ！"})
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=payload)
    requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=payload)
    return render(request, 'html_Appt/Appt_end.html',)

def video(request):
    true_number = Owner_DB.objects.get(owner='Owner')
    context = {'number':true_number.update_url_text}
    return render(request, 'html_Appt/video.html',context)

def save_qrcode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        qrData = data.get('qrData', None)

        headers = {"Content-Type": "application/json"}
        cookies = {"test_cookie": "qrcode"}
        payload = json.dumps({"value1": qrData})
        #if "https://0cab-133-99-163-253.ngrok-free.app/Guest_home/" in qrData:
        if ".ngrok-free.app/Guest_home/" in qrData:
            #デバックの時に使う
            #保存する際のファイル名を指定
            #filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            #f = open('media/appt/'+filename, "w")
            #f.write(qrData)
            #f.close()
            requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=payload)
            requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=payload)
            return JsonResponse({'redirect': True})
        else:
            #デバックの時に使う
            #保存する際のファイル名を指定
            #filename = f"NG{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            #f = open('media/appt/'+filename, "w")
            #f.write(qrData)
            #f.close()
            return JsonResponse({'redirect': False,'message':'QRコードが登録されていません<br>正しいQRコードを読み込んでください'})
    return JsonResponse({'message': 'スナップショットの保存に失敗しました。'}, status=400)

def save_geolocation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)

#        data_1 = Owner_DB.objects.get(location=payload)
#        Owner_data = json.loads(data_1)
#        Owner_latitude = Owner_data.get('latitude', None)
#        Owner_longitude = Owner_data.get('longitude', None)
#        data_1 = request.body
        true_number = Owner_DB.objects.get(owner='Owner')
        data_1 = true_number.location
        Owner_data = json.loads(data_1)
        Owner_latitude = Owner_data.get('latitude', None)
        Owner_longitude = Owner_data.get('longitude', None)

        #if latitude - 0.00045 <= Owner_latitude < latitude + 0.00045 and longitude - 0.0005 <= Owner_longitude < longitude + 0.0005:
        num = 0.0005**2 + 0.00045**2
        r = ((latitude-Owner_latitude)**2 + (longitude-Owner_longitude)**2)
        if r <= num:
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


def check_video_status(request):
    if request.is_ajax():
        # レコードの最新のvideo_statusを取得
        latest_appt = Appt_DB.objects.latest('pk')
        data = {
            'video_status': latest_appt.video_status,
        }
        return JsonResponse(data)
