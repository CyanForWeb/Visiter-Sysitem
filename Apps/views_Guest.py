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
            requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
            return render(request, 'html_Guest/Guest_other_form2.html')
        #form2内容をdbに保存して、for3に遷移
        if "form2_submit" in request.POST: #ボタンが押されたら...
            form2_name = request.POST.get('form2_name')
            form2_address = request.POST.get('form2_address')
            Other_DB.objects.update(form2_name=form2_name,
                                    form2_address=form2_address) #Other_DBに値を保存
            #POSTリクエストを送信　質問フォーム2が送信されたら：住民に通知
            headers = {"Content-Type": "application/json"}
            cookies = {"test_cookie": "aaa"}
            data = json.dumps({"value1": "名前、住所、連絡先が入力されました！"})
            #住民のiftttのkeyを入力する↓
            requests.post("https://maker.ifttt.com/trigger/hello/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies, data=data)
            return render(request, 'html_Guest/Guest_other_form3.html')
    return render(request, 'html_Guest/Guest_other_form1.html')

def other_form4(request): #質問フォーム3→4に移る時に使う
    if request.method == 'GET':
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
    context = {}
    if request.method == 'GET':
        time_status = 0
        if Owner_Time_DB.objects.filter(start_date__lte=datetime.now().date(),finish_date__gte=datetime.now().date()):
            time_status = 1
        context = {"time_status":time_status}
    return render(request, 'html_Guest/Guest_delivery.html', context)

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
     
    requests.post("https://maker.ifttt.com/trigger/post/with/key/bmJJC2vwlzldgPEhoZmrk3")
    headers = {"Content-Type": "application/json"}
    cookies = {"test_cookie": "aaa"}
    data = json.dumps({"value1": "宛名がある郵便物が投函されました！"})
    #住民のiftttのkeyを入力する↓
    #requests.post("https://maker.ifttt.com/trigger/post/with/key/bmJJC2vwlzldgPEhoZmrk3", headers=headers, cookies=cookies)
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
            return JsonResponse({'redirect': False,'message':'QRコードに近づいて再読み込みしてください。'})
    return JsonResponse({'message': '位置情報が取得できませんでした。'}, status=400)
