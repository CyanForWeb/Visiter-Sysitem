from django.conf import settings
from django.db import models
from django.utils import timezone


#住人　Webアプリに使用するもの
class Owner_DB(models.Model):
    owner = models.TextField(default="Owner")
    location = models.TextField()
    def __str__(self):
        return self.owner

class Owner_Time_DB(models.Model):
    owner = models.TextField(default="Owner")
    start_date = models.DateTimeField(blank=True, null=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.owner+":"+str(self.start_date)+"~"+str(self.finish_date)

#客人からの通知を保存するために使用する
class Visitor_DB(models.Model):
    visitor = models.TextField(max_length=10)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.visitor+":"+str(self.date)

class Visitor_Message_DB(models.Model):
    visitor = models.TextField(max_length=10)
    message = models.TextField(max_length=20)
    def __str__(self):
        return self.visitor

class Appt_DB(models.Model):
    visitor = models.TextField(default="Appt")
    date = models.DateTimeField(default=timezone.now)
    finish_date = models.DateTimeField(default=timezone.now)
    video_status = models.IntegerField(default=0)
    def __str__(self):
        return self.visitor+":"+str(self.date)

class Delivery_DB(models.Model):
    visitor = models.TextField(default="Delivery")
    date = models.DateTimeField(default=timezone.now)
    img = models.ImageField(upload_to="delivery", blank=True, null=True)
    def __str__(self):
        return self.visitor+":"+str(self.date)

class Post_DB(models.Model):
    visitor = models.TextField(max_length=10)
    date = models.DateTimeField(default=timezone.now)
    img = models.ImageField(upload_to="post", blank=True, null=True)
    def __str__(self):
        return self.visitor+":"+str(self.date)

class Other_DB(models.Model):
    visitor = models.TextField(default="Other")
    date = models.DateTimeField(default=timezone.now)
    video_status = models.IntegerField(default=0)
    form1 = models.TextField(max_length=500)
    form2_name = models.TextField(max_length=50)
    form2_address = models.TextField(max_length=50)
    form2_contact = models.TextField(max_length=50)
    form3 = models.TextField(max_length=10)
    form4_date = models.TextField(max_length=20)
    form4_day = models.TextField(max_length=20)
    form4_weather = models.TextField(max_length=20)
    form4_transportation = models.TextField(max_length=50)
    form4_trivia = models.TextField(max_length=300)
    form4_message = models.TextField(max_length=300)
    def __str__(self):
        return self.visitor+":"+str(self.date)
