# Generated by Django 3.2.6 on 2021-11-20 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=32)),
                ('port', models.CharField(max_length=32)),
                ('hide', models.BooleanField(default=False)),
            ],
        ),
    ]
