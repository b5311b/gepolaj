# Generated by Django 3.1 on 2020-10-18 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0017_auto_20201018_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminlist',
            name='comp',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='adminlist',
            name='lead',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='adminlist',
            name='mach',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='adminlist',
            name='samp',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
