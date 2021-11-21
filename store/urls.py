from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.Store.as_view(),name='index'),
    path('order-history/', views.History.as_view(),name='history'),
]
