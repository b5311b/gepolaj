# Generated by Django 3.1 on 2020-10-11 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0007_auto_20201011_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machinery',
            name='cidentnum',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='machinery',
            name='run_hist',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
