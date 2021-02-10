# Generated by Django 3.1 on 2020-09-24 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0004_auto_20200907_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='machinery',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='drivers', to='machines.machinery'),
        ),
    ]
