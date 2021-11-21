from django.shortcuts import render
from django.views.generic import View
from .models import Product

class Store(View):
    template_name = 'store/store.html'

    def get(self,request,*args, **kwargs):
        query = Product.objects.all()
        ctx = {
            'products':query
        }
        return render(request,self.template_name,ctx)
    

class History(View):
    template_name = 'store/order_history.html'

    def get(self,request,*args, **kwargs):
        ctx = {}
        return render(request,self.template_name,ctx)