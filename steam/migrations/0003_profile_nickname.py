# Generated by Django 3.2.6 on 2021-08-27 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steam', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]