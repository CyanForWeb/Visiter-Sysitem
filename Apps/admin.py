from django.contrib import admin
from .models import *

#住人　Webアプリに使用するもの
admin.site.register(Owner_DB)
admin.site.register(Owner_Time_DB)


#客人からの通知を保存するために使用する
admin.site.register(Visitor_DB)
admin.site.register(Visitor_Message_DB)
admin.site.register(Appt_DB)
admin.site.register(Delivery_DB)
admin.site.register(Post_DB)
admin.site.register(Other_DB)
