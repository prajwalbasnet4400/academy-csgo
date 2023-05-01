# Generated by Django 3.2.6 on 2023-04-30 15:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pay_khalti',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='pay_stripe',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='StripePurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer', models.CharField(max_length=54, null=True)),
                ('receiver', models.CharField(max_length=54, null=True)),
                ('idx', models.CharField(max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='KhaltiPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer', models.CharField(max_length=54, null=True)),
                ('receiver', models.CharField(max_length=54, null=True)),
                ('idx', models.CharField(max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
