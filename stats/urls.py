from django.urls import path
from . import views

app_name = 'stats'

urlpatterns = [
    path('',views.Index.as_view(),name='index'),
    path('servers/',views.Servers.as_view(),name='servers'),
    path('premium/',views.VipListView.as_view(),name='premium'),
    path('stats/retake/',views.Retake.as_view(),name='retake'),
    path('stats/deathmatch/',views.Deathmatch.as_view(),name='deathmatch'),
    path('profile/<int:steam>/',views.ProfileView.as_view(),name='profile'),
    path('misc/report-player/',views.Report.as_view(),name='report'),
    path('misc/appeal-ban/',views.Appeal.as_view(),name='appeal'),
    path('misc/contact/',views.Contact.as_view(),name='contact'),
]
