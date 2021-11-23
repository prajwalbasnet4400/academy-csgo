from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.PremiumStore.as_view(),name='index'),
    path('product/<slug:slug>/', views.ProductView.as_view(),name='product'),
    path('checkout/<slug:slug>/', views.CheckoutView.as_view(),name='checkout'),
    path('verify/', views.KhaltiVerifyView.as_view(),name='khalti_verification_url'),
    # path('order-history/', views.History.as_view(),name='history'),
]
