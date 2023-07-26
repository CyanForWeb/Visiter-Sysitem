from django.conf import settings
from django.db import models
from django.utils import timezone

#これは使用しない（例）
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

#住人　Webアプリに使用するもの


#アポ済み　Webアプリに使用するもの


#客人　Webアプリに使用するもの
