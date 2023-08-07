from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Apps.urls')),
]

# modelsのImageFieldにpicを格納する機能で使用
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
