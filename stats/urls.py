from django.urls import path
from . import views

app_name = 'stats'

urlpatterns = [
    path('',views.Index.as_view(),name='index'),
    path('servers/',views.ServerView.as_view(),name='servers'),
    path('premium/',views.VipListView.as_view(),name='premium'),
    path('stats/retake/',views.RetakeView.as_view(),name='retake'),
    path('stats/warmup/',views.WarmupView.as_view(),name='deathmatch'),
    path('profile/<int:steamid64>/',views.ProfileView.as_view(),name='profile'),
    path('misc/report-player/',views.ReportView.as_view(),name='report'),
    path('misc/appeal-ban/',views.AppealView.as_view(),name='appeal'),
    path('misc/contact/',views.ContactView.as_view(),name='contact'),
]