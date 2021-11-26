from django.core.management.base import BaseCommand
import datetime
from stats.models import Vip,SmAdmins

def notify(days):
    return datetime.date.today() + datetime.timedelta(days=days)

class Command(BaseCommand):
    help = 'check and delete expired premium subs'

    def handle(self, *args, **kwargs):
        queryset = Vip.objects.filter(expires__lte = notify(-1))
        for obj in queryset:
            admin = SmAdmins.objects.using(obj.server.db_identifier).get(identity=obj.steamid)
            admin.delete()
            obj.delete()