from django.contrib.auth.models import AbstractUser
from django.db import models
from stats.functions import get_profile

class User(AbstractUser):
    
    @staticmethod
    def convert_to_steamid(steamid64):
        y = int(steamid64) - 76561197960265728
        x = y % 2 
        return "STEAM_1:{}:{}".format(x, (y - x) // 2)



class Profile(models.Model):
    steamid = models.CharField(primary_key=True, max_length=22)
    avatar = models.URLField(null=True,blank=True)
    nickname = models.CharField(max_length=64,blank=True,null=True,db_collation='utf8mb4_general_ci')
    last_updated = models.DateTimeField(auto_now_add=True)

    def get_steamid64(self):
        x , y , z = self.steamid.split(':')
        return int(z) * int(2) + int(y) + 76561197960265728

    def save(self,*args, **kwargs):
        profile = get_profile(self.get_steamid64())
        self.avatar = profile.get('avatarfull',None)
        self.nickname = profile.get('personaname',None)
        super(Profile,self).save(*args, **kwargs)

    def __str__(self):
        return self.steamid