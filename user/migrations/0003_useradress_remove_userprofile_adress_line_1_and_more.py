# Generated by Django 4.1.1 on 2022-12-09 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAdress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress_line_1', models.CharField(blank=True, max_length=100)),
                ('adress_line_2', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=20)),
                ('state', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='adress_line_1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='adress_line_2',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='city',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='state',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='adress',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.useradress'),
        ),
    ]
