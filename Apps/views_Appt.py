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
    return render(request, 'html_Appt/Appt_end.html',)

def save_qrcode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        qrData = data.get('qrData', None)

        headers = {"Content-Type": "application/json"}
        cookies = {"test_cookie": "qrcode"}
        payload = json.dumps({"value1": qrData})
        if ".org" in qrData:
            #デバックの時に使う
            #保存する際のファイル名を指定
            #filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            #f = open('media/appt/'+filename, "w")
            #f.write(qrData)
            #f.close()
            requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=payload)
            return JsonResponse({'redirect': True})
        else:
            #デバックの時に使う
            #保存する際のファイル名を指定
            #filename = f"NG{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            #f = open('media/appt/'+filename, "w")
            #f.write(qrData)
            #f.close()
            return JsonResponse({'redirect': False,'message':'QRコードが登録されていません。正しいQRコードを読み込んでください。'})
    return JsonResponse({'message': 'スナップショットの保存に失敗しました。'}, status=400)

def save_geolocation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude', None)
        longitude = data.get('longitude', None)

        if 35.5000000 <= latitude < 36.050000 and 139.000000 <= longitude < 140.000000:
            #デバックの時に使う
            #保存する際のファイル名を指定
            #filename = f"OK_GEO_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            #f = open('media/appt/'+filename, "w")
            #f.write("request.body:")
            #f.write(json.dumps(data))
            #f.close()

            #requests.post("https://maker.ifttt.com/trigger/hello/with/key/dPMcKW7OLMVpEKmN9HwjxZ", headers=headers, cookies=cookies, data=payload)
            return JsonResponse({'redirect': True})
        else:
            #デバックの時に使う
            #保存する際のファイル名を指定
            #filename = f"NG_GEO_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            #f = open('media/appt/'+filename, "w")
            #f.write("request.body:")
            #f.write(json.dumps(data))
            #f.close()
            return JsonResponse({'redirect': False,'message':'位置情報が正しくありません。'})
    return JsonResponse({'message': '位置情報が取得できませんでした。'}, status=400)


def check_video_status(request):
    if request.is_ajax():
        # レコードの最新のvideo_statusを取得
        latest_appt = Appt_DB.objects.latest('pk')
        data = {
            'video_status': latest_appt.video_status,
        }
        return JsonResponse(data)
