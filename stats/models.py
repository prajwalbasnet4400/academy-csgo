from django.db import models
from django.utils.text import slugify
from steam.models import Profile
from . import resolver
from . import vip
import datetime

class Server(models.Model):
    ip = models.CharField(max_length=32)
    port = models.CharField(max_length=32)
    hide = models.BooleanField(default=False)
    display_name = models.CharField(unique=True,max_length=128)
    ssh_ip = models.CharField(max_length=128,null=True,blank=True)
    ssh_port = models.IntegerField(null=True,blank=True)
    ssh_user = models.CharField(max_length=64,null=True,blank=True)
    ssh_psswd = models.CharField(max_length=64,null=True,blank=True)
    path_to_vip_file = models.CharField(max_length=512,null=True,blank=True)
    selling_premium = models.BooleanField(default=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return f'{self.display_name}'

    def save(self,*args, **kwargs):
        self.slug = slugify(self.display_name)
        super().save(*args, **kwargs)


def get_expiry():
    return datetime.date.today() + datetime.timedelta(days=31)

class Vip(models.Model):
    profile_url = models.CharField(max_length=256,null=False,blank=False)
    name = models.CharField(max_length=128,blank=True,null=True)
    steamid = models.CharField(max_length=256,blank=True,null=True)
    steamid64 = models.CharField(max_length=128,blank=True,null=True)
    avatar = models.URLField(null=True,blank=True)
    dateofpurchase = models.DateField(default=datetime.date.today)
    expires = models.DateField(default=get_expiry())
    active = models.BooleanField(default=True)
    server = models.ForeignKey(Server,on_delete=models.CASCADE)
    discord_id = models.CharField(max_length=32,blank=True,null=True)

    def __str__(self):
        return self.name

    def to_expire(self):
        delta= self.expires - datetime.date.today()
        return delta.days

    def save(self,*args, **kwargs):
        data = resolver.get_playerinfo(self.profile_url)
        self.name = data.get('personaname')
        self.steamid64 = data.get('steamid')
        self.steamid = resolver.convert_to_steamid(data.get('steamid'))
        self.avatar = data.get('avatarfull')

        if self.pk:
            query = Vip.objects.get(pk=self.pk)
            if query.active == self.active:
                pass
            elif self.active == True:
                print('asudghaiushgdiouashgdiuh')
                # vip.add_vip(self.steamid,self.server)
            else:
                pass
                # vip.del_vip(self.steamid,self.server)
                
        # If new entry add the VIP to the server file
        else:
            pass
            # vip.add_vip(self.steamid)
        super().save(*args, **kwargs)

class LvlBase(models.Model):
    steam = models.CharField(primary_key=True, max_length=22, db_collation='utf8_unicode_ci')
    name = models.CharField(max_length=32)
    value = models.IntegerField()
    rank = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    shoots = models.IntegerField()
    hits = models.IntegerField()
    headshots = models.IntegerField()
    assists = models.IntegerField()
    round_win = models.IntegerField()
    round_lose = models.IntegerField()
    playtime = models.IntegerField()
    lastconnect = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'lvl_base'

    def get_playtime(self):
        pt = self.playtime // 3600
        return pt
    
    def get_rank(self):
        return LvlBase.objects.using('retake').values('value').filter(value__gte=self.value).count()
    
    def get_rank_retake(self):
        return LvlBase.objects.using('retake').values('value').filter(value__gte=self.value).count()
    
    def get_rank_warmup(self):
        return LvlBase.objects.using('warmup').values('value').filter(value__gte=self.value).count()
    
    def get_steamid64(self):
        x , y , z = self.steam.split(':')
        return int(z) * int(2) + int(y) + 76561197960265728
    
    def get_kd(self):
        kills = self.kills
        deaths = self.deaths
        try:
            return round(int(kills) / int(deaths),2)
        except (ValueError, ZeroDivisionError):
            return 0
    
    def get_accuracy(self):
        shoot = self.shoots
        hit = self.hits
        try:
            return int(round((int(hit) / int(shoot)),2)*100)
        except (ValueError, ZeroDivisionError):
            return 0
    
    def get_avatar(self):
        obj, created = Profile.objects.get_or_create(steamid=self.steam)
        return obj.avatar