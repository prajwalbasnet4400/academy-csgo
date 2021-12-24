import datetime
from stats.models import Vip
from store.models import Product, Purchase

def add_vip(product_slug,khalti_idx,steamid,steamid64,name,avatar,**kwargs):
    product = Product.objects.get(slug=product_slug)
    expires_date = datetime.timedelta(days=product.duration) + datetime.date.today()
    Purchase.objects.create(idx=khalti_idx,product=product,receiver=steamid,**kwargs)
    obj,created = Vip.objects.get_or_create(steamid=steamid,server=product.server,
                                            defaults={'expires':expires_date,
                                            'name':name,'steamid64':steamid64,'avatar':avatar})

    if not created:
        obj.expires = obj.expires + datetime.timedelta(days=product.duration)
        obj.save()