# Generated by Django 3.1 on 2020-10-16 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0015_auto_20201015_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runing',
            name='end_time',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='runing',
            name='start_time',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
