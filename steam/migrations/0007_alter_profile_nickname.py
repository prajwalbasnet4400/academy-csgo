# Generated by Django 3.2.6 on 2021-08-28 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('steam', '0006_alter_profile_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, db_collation='utf8_general_ci', max_length=64, null=True),
        ),
    ]
