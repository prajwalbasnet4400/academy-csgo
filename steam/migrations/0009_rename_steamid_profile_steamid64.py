# Generated by Django 3.2.6 on 2021-11-22 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('steam', '0008_auto_20210902_1434'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='steamid',
            new_name='steamid64',
        ),
    ]
