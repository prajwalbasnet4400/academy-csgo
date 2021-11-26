from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.http.response import HttpResponse
from django.views.generic import View, ListView, DetailView
from django.contrib import messages

from stats.models import Server
from stats.resolver import get_playerinfo

from .models import Product
from .logic import premium,khalti

class PremiumStore(ListView):
    template_name = 'store/premium_store.html'
    queryset = Server.objects.filter(selling_premium=True)
    context_object_name = 'servers'
    
    def post(self,request,*args, **kwargs):
        steamid = get_playerinfo(request.POST.get('steamid'))
        if not steamid:
            messages.add_message(request,messages.ERROR,'Error Fetching SteamID',extra_tags='Failure')
            return redirect('store:index')
        product = request.POST.get('product','error')
        return redirect('store:checkout',slug=product,steamid=steamid.get('steamid','error'))    

class CheckoutView(DetailView):
    template_name = 'store/checkout.html'
    model = Product
    context_object_name = 'product'
    
    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model,slug=kwargs.get('slug'))
        if not obj.in_stock():
            return redirect('store:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        steamid = self.kwargs.get('steamid')
        context['profile'] = get_playerinfo(steamid)
        return context
    

class KhaltiVerifyView(View):
    key = settings.KHALTI_API_SECRET_KEY_TEST
    url = 'https://khalti.com/api/v2/payment/verify/'

    def post(self,request,*args, **kwargs):
        data = request.POST
        payload = {"token": data.get('token'),"amount": data.get('amount')}
        response = khalti.verify_khalti(payload)
        if not response.get('success'):                                     # If the provided token is invalid return HTTP 400
            return HttpResponse(status=400)

        profile = get_playerinfo(data.get('merchant_extra'))
        if request.user.is_authenticated:
            premium.add_vip(response['data'],profile,buyer=self.request.user.get_steamid().uid)
        else:
            premium.add_vip(response['data'],profile)
            
        return HttpResponse(status=200)