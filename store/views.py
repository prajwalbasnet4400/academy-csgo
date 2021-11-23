from django.http.response import HttpResponse, JsonResponse
from django.views.generic import View, ListView, DetailView
from django.views.generic.base import TemplateView
from stats.models import Server

from stats.resolver import get_playerinfo
from .models import Product, Purchase
from django.conf import settings
from stats.models import Vip
import requests
import datetime

class PremiumStore(ListView):
    template_name = 'store/premium_store.html'
    queryset = Server.objects.filter(selling_premium=True)
    context_object_name = 'servers'

class ProductView(TemplateView):
    template_name = 'store/product.html'

    def post(self,request,*args, **kwargs):
        data = get_playerinfo(request.POST.get('steamid'))
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        server_name = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(server__slug=server_name)
        return context

    

class CheckoutView(DetailView):
    template_name = 'store/checkout.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        steamid = self.request.GET.get('steamid')
        context['profile'] = get_playerinfo(steamid)
        return context
    

class KhaltiVerifyView(View):
    key = settings.KHALTI_API_SECRET_KEY_TEST
    url = 'https://khalti.com/api/v2/payment/verify/'

    def post(self,request,*args, **kwargs):
        data = request.POST
        token = data.get('token')
        amount = data.get('amount')
        profile = data.get('merchant_extra')
        headers = {"Authorization": f"Key {self.key}"}
        payload = {"token": token,"amount": amount}
        response = requests.post(self.url, payload, headers = headers)
        response = response.json()
        if response.get('idx',None):
            prdt = Product.objects.get(slug=response.get('product_identity'))
            Purchase.objects.create(idx=response.get('idx'),product=prdt,mobile=data.get('mobile',None),token=token)
            expires_date = datetime.timedelta(days=prdt.duration) + datetime.date.today()
            obj,created = Vip.objects.get_or_create(profile_url=profile,server=prdt.server,defaults={'expires':expires_date})
            if not created:
                obj.expires = obj.expires + datetime.timedelta(days=prdt.duration)
                obj.save()
        return HttpResponse(response)
