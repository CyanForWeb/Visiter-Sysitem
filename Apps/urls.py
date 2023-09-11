from django.urls import path
from . import views_Appt, views_Guest, views_Owner

urlpatterns = [

#住民のWebアプリに使用するURL
    path('Owner_home', views_Owner.home, name='Owner_home'),#一番最初にアクセスする画面
    path('Owner_setting', views_Owner.setting, name='Owner_setting'),
    path('Owner_setting_time', views_Owner.setting_time, name='Owner_setting_time'),
    path('Owner_setting_home', views_Owner.setting_home, name='Owner_setting_home'),
    path('Owner_setting_end', views_Owner.setting_end, name='Owner_setting_end'),
    path('Owner_seeform', views_Owner.seeform, name='Owner_seeform'),
    #path('Owner_seeform_detail', views_Owner.seeform_detail, name='Owner_seeform_detail'),
    path('<int:id>', views_Owner.seeform_detail, name='Owner_seeform_detail'),
    path('VideoChat', views_Owner.videochat, name='VideoChat'),


#アポ済みのWebアプリに使用するURL
    path('Appt_home', views_Appt.home, name='Appt_home'),#一番最初にアクセスする画面
    path('Appt_end', views_Appt.end, name='Appt_end'),#最後の画面
    path('save_qrcode/', views_Appt.save_qrcode, name='save_qrcode'),
    path('save_geolocation/', views_Appt.save_geolocation, name='save_geolocation'),
    path('check_video_status', views_Appt.check_video_status, name='check_video_status'),#ビデオステータスの確認

#客人のWebアプリに使用するURL
    path('Guest_home', views_Guest.home, name='Guest_home'),#一番最初にアクセスする画面
    #その他　客人画面
    path('Guest_other', views_Guest.other, name='Guest_other'),#質問フォーム開始画面
    path('Guest_other_form', views_Guest.other_form, name='Guest_other_form'),
    path('Guest_other_form4', views_Guest.other_form4, name='Guest_other_form4'),
    path('other_check_video_status', views_Guest.other_check_video_status, name='other_check_video_status'),#ビデオステータスの確認
    #配達員　画面
    path('Guest_delivery', views_Guest.delivery, name='Guest_delivery'),#ハンコ有無の確認画面
    path('Guest_delivery_camera', views_Guest.delivery_camera, name='Guest_delivery_camera'),#宛名カメラ判定画面
    path('Guest_delivery_end1', views_Guest.delivery_end1, name='Guest_delivery_end1'),#最後の画面
    #ポスト投函　画面
    path('Guest_post', views_Guest.post, name='Guest_post'),#宛名カメラ判定画面
    path('Guest_post_end1', views_Guest.post_end1, name='Guest_post_end1'),#最後の画面１
    path('Guest_post_pic', views_Guest.post_pic, name='Guest_post_pic'),#投函物写真撮って送る画面
    path('Guest_post_end2', views_Guest.post_end2, name='Guest_post_end2'),#最後の画面２

#カメラ機能で使用するURL
    path('save_snapshot/', views_Guest.save_snapshot, name='save_snapshot'),
]
