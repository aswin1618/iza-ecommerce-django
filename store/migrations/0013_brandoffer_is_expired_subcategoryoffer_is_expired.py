# Generated by Django 4.1.1 on 2022-12-29 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_rename_price_product_stock_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='brandoffer',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subcategoryoffer',
            name='is_expired',
            field=models.BooleanField(default=False),
        ),
    ]
