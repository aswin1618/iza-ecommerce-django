# Generated by Django 4.1.1 on 2022-12-30 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0023_alter_product_brand_offer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='color',
            field=models.CharField(choices=[('red', 'red'), ('orange', 'orange'), ('yellow', 'yellow'), ('green', 'green'), ('cyan', 'cyan'), ('azure', 'azure'), ('blue', 'blue'), ('violet', 'violet'), ('magenta', 'magenta'), ('pink', 'pink'), ('black', 'black')], default='null', max_length=100),
        ),
    ]
