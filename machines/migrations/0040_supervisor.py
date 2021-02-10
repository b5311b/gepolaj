# Generated by Django 3.1 on 2021-01-18 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0039_auto_20210114_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('wday', models.DateField(auto_now_add=True)),
                ('user', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]
