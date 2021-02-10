# Generated by Django 3.1 on 2020-10-15 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0014_auto_20201015_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runing',
            name='end_kmeter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='runing',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='runing',
            name='start_kmeter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='runing',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='runing',
            name='wtype',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
