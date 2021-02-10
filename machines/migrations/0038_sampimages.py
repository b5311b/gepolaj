# Generated by Django 3.1 on 2021-01-12 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('machines', '0037_auto_20201214_0013'),
    ]

    operations = [
        migrations.CreateModel(
            name='SampImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_Img', models.ImageField(upload_to='images/')),
                ('oilsamples', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sampleimages', to='machines.oilsamples')),
            ],
        ),
    ]