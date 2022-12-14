# Generated by Django 4.1.1 on 2022-12-28 23:00

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_product_brand_offer_product_sub_category_offer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='sub_category_offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.subcategoryoffer'),
        ),
        migrations.CreateModel(
            name='BrandOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category_offer', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.brand')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand_offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.brandoffer'),
        ),
    ]
