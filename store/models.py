from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from steam.models import User
from stats.models import Server

class Product(models.Model):
    title = models.CharField(max_length=64,unique=True)
    detail = models.CharField(max_length=64)
    price = models.PositiveSmallIntegerField()
    features = models.TextField(help_text='Displayed in a list, create newline to separate list')
    notes = models.CharField(max_length=128, blank=True,help_text='Displayed highlighted at the end of features list')
    icon = models.CharField(max_length=32,blank=True,null=True,help_text='Font awesome 5 class name like so "fas fa-hammer")')
    image = models.ImageField(upload_to='uploads/',null=True,blank=True)
    slug = models.SlugField(unique=True,blank=True)
    server = models.ForeignKey(Server,on_delete=models.CASCADE,null=True)
    duration = models.PositiveSmallIntegerField()


    def save(self,*args, **kwargs):
        slug = f"{self.server.slug}-{self.duration}D"
        self.slug = slugify(slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:checkout", kwargs={"slug": self.slug})

class Purchase(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    idx = models.CharField(max_length=128)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=13)
    token = models.CharField(max_length=128)