from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('stats.urls')),
    path('store/',include('store.urls')),
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
