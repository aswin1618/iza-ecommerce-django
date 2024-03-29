# Generated by Django 4.1.1 on 2023-08-17 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=250)),
                ('cat_image', models.ImageField(blank=True, upload_to='photos/categories')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcat_name', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=100, null=True, unique=True)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
            options={
                'verbose_name': 'subcategory',
                'verbose_name_plural': 'subcategories',
            },
        ),
    ]
