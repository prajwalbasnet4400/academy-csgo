# Generated by Django 3.2.6 on 2021-11-25 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20211125_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveSmallIntegerField(help_text='Enter in paisa. ie Rs 10 is 1000'),
        ),
    ]
