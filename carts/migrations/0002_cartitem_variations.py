# Generated by Django 4.1.1 on 2022-11-17 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_delete_variationmanager'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variation'),
        ),
    ]
