# Generated by Django 4.1.1 on 2022-12-28 23:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_brand_alter_product_sub_category_offer_brandoffer_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brandoffer',
            old_name='sub_category_offer',
            new_name='brand_offer',
        ),
    ]
