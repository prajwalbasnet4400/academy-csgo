# Generated by Django 3.2.6 on 2021-11-21 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_auto_20211121_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='ssh_ip',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
