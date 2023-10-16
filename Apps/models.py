from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import datetime

#住人　Webアプリに使用するもの
class Owner_DB(models.Model):
    owner = models.TextField(default="Owner")
    location = models.TextField(null=True)
    update_url_text = models.IntegerField(default='11')
    def __str__(self):
        return self.owner

class Owner_Time_DB(models.Model):
    owner = models.TextField(default="Owner")
    start_date = models.DateField(verbose_name="日付", null=True)
    start_time = models.TimeField(verbose_name="時刻", null=True)
    finish_date = models.DateField(verbose_name="日付", null=True)
    finish_time = models.TimeField(verbose_name="時刻", null=True)
    def __str__(self):
        return self.owner+":"+f"{self.start_date.strftime('%Y年%m月%d日%H時%M分%S秒')}"+"~"+f"{self.finish_date.strftime('%Y年%m月%d日%H時%M分%S秒')}"

#客人からの通知を保存するために使用する
class Visitor_DB(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    visitor = models.TextField(max_length=10)
    date = models.DateTimeField(null=True)
    message = models.TextField(max_length=20, null=True)
    def __str__(self):
        #return self.visitor+":"+f"{self.date.strftime('%Y年%m月%d日%H時%M分%S秒')}"
        return self.visitor

class Visitor_Message_DB(models.Model):
    visitor = models.TextField(max_length=10)
    message = models.TextField(max_length=50)
    def __str__(self):
        return self.visitor

class Appt_DB(models.Model):
    visitor = models.TextField(default="Appt")
    date = models.DateTimeField(null=True)
    video_status = models.IntegerField(default=0)
    def __str__(self):
        #return self.visitor+":"+f"{self.date.strftime('%Y年%m月%d日%H時%M分%S秒')}"
        return self.visitor

class Delivery_DB(models.Model):
    visitor = models.TextField(default="Delivery")
    date = models.DateTimeField(null=True)
    img = models.ImageField(upload_to="delivery", blank=True, null=True)
    def __str__(self):
        return self.visitor+":"+f"{self.date.strftime('%Y年%m月%d日%H時%M分%S秒')}"

class Post_DB(models.Model):
    visitor = models.TextField(max_length=10)
    date = models.DateTimeField(null=True)
    img = models.ImageField(upload_to="post/", blank=True, null=True)
    def __str__(self):
        return self.visitor+"："+f"{self.date.strftime('%Y年%m月%d日%H時%M分%S秒')}"

class Other_DB(models.Model):
    visitor = models.TextField(default="Other")
    date = models.DateTimeField(default="未回答")
    video_status = models.IntegerField(default=0)
    form1 = models.TextField(max_length=500, default="未回答")
    form2_name = models.TextField(max_length=50, default="未回答")
    form2_address = models.TextField(max_length=50, default="未回答")
    form3 = models.TextField(max_length=10, default="未回答")
    form4_date = models.TextField(max_length=20, default="未回答")
    form4_day = models.TextField(max_length=20, default="未回答")
    form4_weather = models.TextField(max_length=20, default="未回答")
    form4_transportation = models.TextField(max_length=50, default="未回答")
    form4_trivia = models.TextField(max_length=300, default="未回答")
    form4_message = models.TextField(max_length=300, default="未回答")
    def __str__(self):
        return self.visitor+":"+f"{self.date.strftime('%Y年%m月%d日%H時%M分%S秒')}"
