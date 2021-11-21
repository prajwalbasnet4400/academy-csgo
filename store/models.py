from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=64)
    detail = models.CharField(max_length=64)
    price = models.SmallIntegerField()
    features = models.TextField(help_text='Displayed in a list, create newline to separate list')
    notes = models.CharField(max_length=128, blank=True,help_text='Displayed highlighted at the end of features list')
    icon = models.CharField(max_length=32,blank=True,null=True,help_text='Font awesome 5 class name like so "fas fa-hammer")')
    razorpay_button = models.TextField(help_text='Razorpay button embed code')

    def __str__(self):
        return self.title