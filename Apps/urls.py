from django.urls import path
from . import views_Appt, views_Guest, views_Owner

urlpatterns = [

#住民のWebアプリに使用するURL
    path('Owner_home', views_Owner.home, name='Owner_home'),#一番最初にアクセスする画面
    path('Owner_setting', views_Owner.setting, name='Owner_setting'),#一番最初にアクセスする画面
    path('Owner_seeform', views_Owner.seeform, name='Owner_seeform'),#一番最初にアクセスする画面

#アポ済みのWebアプリに使用するURL
    path('Appt_home', views_Appt.home, name='Appt_home'),#一番最初にアクセスする画面
    path('Appt_end', views_Appt.end, name='Appt_end'),#最後の画面

#客人のWebアプリに使用するURL
    path('Guest_home', views_Guest.home, name='Guest_home'),#一番最初にアクセスする画面
    #その他　客人画面
    path('Guest_other', views_Guest.other, name='Guest_other'),#質問フォーム開始画面
    path('Guest_other_form1', views_Guest.other_form1, name='Guest_other_form1'),#最後の画面
    path('Guest_other_form2', views_Guest.other_form2, name='Guest_other_form2'),#最後の画面
    path('Guest_other_form3', views_Guest.other_form3, name='Guest_other_form3'),#最後の画面
    path('Guest_other_form4', views_Guest.other_form4, name='Guest_other_form4'),#最後の画面
    path('Guest_other_end', views_Guest.other_end, name='Guest_other_end'),#最後の画面
    #配達員　画面
    path('Guest_delivery', views_Guest.delivery, name='Guest_delivery'),#宛名カメラ判定画面
    path('Guest_delivery_stamp', views_Guest.delivery_stamp, name='Guest_delivery_stamp'),#ハンコ有無の確認画面
    path('Guest_delivery_end1', views_Guest.delivery_end1, name='Guest_delivery_end1'),#最後の画面
    #ポスト投函　画面
    path('Guest_post', views_Guest.post, name='Guest_post'),#宛名カメラ判定画面
    path('Guest_post_end1', views_Guest.post_end1, name='Guest_post_end1'),#最後の画面１
    path('Guest_post_pic', views_Guest.post_pic, name='Guest_post_pic'),#投函物写真撮って送る画面
    path('Guest_post_end2', views_Guest.post_end2, name='Guest_post_end2'),#最後の画面２
]
