# Generated by Django 3.2.6 on 2021-08-27 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LvlBase',
            fields=[
                ('steam', models.CharField(db_collation='utf8_unicode_ci', max_length=22, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('value', models.IntegerField()),
                ('rank', models.IntegerField()),
                ('kills', models.IntegerField()),
                ('deaths', models.IntegerField()),
                ('shoots', models.IntegerField()),
                ('hits', models.IntegerField()),
                ('headshots', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('round_win', models.IntegerField()),
                ('round_lose', models.IntegerField()),
                ('playtime', models.IntegerField()),
                ('lastconnect', models.IntegerField()),
            ],
            options={
                'db_table': 'lvl_base',
                'managed': False,
            },
        ),
    ]
