# Generated by Django 4.1.1 on 2022-12-15 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_useradress_district_useradress_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useradress',
            name='pin_code',
            field=models.IntegerField(max_length=10, null=True),
        ),
    ]
