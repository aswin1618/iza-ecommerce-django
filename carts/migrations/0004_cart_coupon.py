# Generated by Django 4.1.1 on 2022-12-30 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_alter_brandoffer_brand_and_more'),
        ('carts', '0003_cart_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.coupon'),
        ),
    ]
