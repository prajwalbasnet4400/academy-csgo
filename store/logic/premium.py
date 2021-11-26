import datetime
from stats.models import Vip, SmAdmins
from store.models import Product, Purchase
from stats.functions import get_steamid


def add_vip(response,profile,**kwargs):
    product_pk = response.get('product_identity')
    product = Product.objects.get(pk=product_pk)

    steamid = get_steamid(profile.get('steamid'))
    steamid64 = profile.get('steamid')
    name = profile.get('personaname')
    avatar = profile.get('avatarfull')
    expires_date = datetime.timedelta(days=product.duration) + datetime.date.today()

    SmAdmins.objects.using(product.server.db_identifier).get_or_create(authtype='steam',identity=steamid,flags='ao',name=name,immunity=0)
    Purchase.objects.create(idx=response.get('idx'),product=product,receiver=steamid,**kwargs)
    obj,created = Vip.objects.get_or_create(steamid=steamid,server=product.server,defaults={'expires':expires_date,'name':name,'steamid64':steamid64,'avatar':avatar})

    if not created:
        obj.expires = obj.expires + datetime.timedelta(days=product.duration)
        obj.save()