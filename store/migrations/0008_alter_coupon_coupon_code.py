# Generated by Django 4.1.1 on 2022-12-28 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='coupon_code',
            field=models.CharField(max_length=15),
        ),
    ]
