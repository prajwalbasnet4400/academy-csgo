import datetime
from django.db import models

from django.utils.text import slugify

from steam.models import Profile

class Server(models.Model):
    display_name = models.CharField(max_length=128,blank=False)
    identifier = models.CharField(max_length=128,unique=True,null=True,blank=False)
    db_identifier = models.CharField(max_length=128,unique=True,null=True,blank=False)
    ip = models.CharField(max_length=32)
    port = models.CharField(max_length=32)
    hide = models.BooleanField(default=False)
    selling_premium = models.BooleanField(default=True)
    slug = models.SlugField(unique=True,null=False,blank=True)

    def __str__(self):
        return f'{self.display_name}'

    def save(self,*args, **kwargs):
        self.slug = slugify(self.identifier)
        super().save(*args, **kwargs)
    
    def product_in_stock(self):
        q = Vip.objects.filter(server=self).count()
        return True if q < 15 else False


def get_expiry():
    return datetime.date.today() + datetime.timedelta(days=30)

class Vip(models.Model):
    name = models.CharField(max_length=128)
    steamid = models.CharField(max_length=256)
    steamid64 = models.CharField(max_length=128)
    avatar = models.URLField(null=True,blank=True)
    dateofpurchase = models.DateField(default=datetime.date.today)
    expires = models.DateField(default=get_expiry())
    server = models.ForeignKey(Server,on_delete=models.CASCADE)

    class Meta:
        ordering = ('expires',)

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        super().save(*args,**kwargs)
        profile = Profile.objects.filter(steamid64=self.steamid64)
        flag = 'ao'
        if profile.exists():
            if profile.first().is_staff:
                flag = 'abcdego'

        obj , created = SmAdmins.objects.using(self.server.db_identifier).get_or_create(authtype='steam',identity=self.steamid,name=self.name,immunity=0,defaults={'flags':flag})
        if not created:
            obj.flags = flag
            obj.save()
            
    def delete(self,*args, **kwargs):
        q = SmAdmins.objects.using(self.server.db_identifier).get(authtype='steam',identity=self.steamid)
        profile = Profile.objects.filter(steamid64=self.steamid64)
        if profile.exists():
            if profile.first().is_staff:
                flag = 'bcdego'
                q.flags = flag
                q.save()
            else:
                q.delete()

        super().delete(*args, **kwargs)


    def to_expire(self):
        delta= self.expires - datetime.date.today()
        return delta.days



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

    def __str__(self):
        return self.name

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

class SmAdmins(models.Model):
    authtype = models.CharField(max_length=5)
    identity = models.CharField(max_length=65)
    password = models.CharField(max_length=65, blank=True, null=True)
    flags = models.CharField(max_length=30)
    name = models.CharField(max_length=65)
    immunity = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'sm_admins'
        constraints = [models.UniqueConstraint(fields=['authtype','identity'],name='unqiue_admin')]


class SmAdminsGroups(models.Model):
    admin_id = models.PositiveIntegerField(primary_key=True)
    group_id = models.PositiveIntegerField()
    inherit_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sm_admins_groups'
        unique_together = (('admin_id', 'group_id'),)


class SmConfig(models.Model):
    cfg_key = models.CharField(primary_key=True, max_length=32)
    cfg_value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sm_config'


class SmGroupImmunity(models.Model):
    group_id = models.PositiveIntegerField(primary_key=True)
    other_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'sm_group_immunity'
        unique_together = (('group_id', 'other_id'),)


class SmGroupOverrides(models.Model):
    group_id = models.PositiveIntegerField(primary_key=True)
    type = models.CharField(max_length=7)
    name = models.CharField(max_length=32)
    access = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'sm_group_overrides'
        unique_together = (('group_id', 'type', 'name'),)


class SmGroups(models.Model):
    flags = models.CharField(max_length=30)
    name = models.CharField(max_length=120)
    immunity_level = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'sm_groups'


class SmOverrides(models.Model):
    type = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=32)
    flags = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'sm_overrides'
        unique_together = (('type', 'name'),)