# Generated by Django 3.2.6 on 2021-08-28 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steam', '0005_alter_profile_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.TextField(blank=True, null=True),
        ),
    ]
