# Generated by Django 1.9 on 2016-05-31 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bags', '0002_auto_20160531_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='arrival_time',
            field=models.CharField(blank=True, max_length=200, verbose_name='Arrival time'),
        ),
        migrations.AlterField(
            model_name='company',
            name='comment',
            field=models.CharField(blank=True, max_length=200, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='company',
            name='giveaways',
            field=models.CharField(blank=True, max_length=200, verbose_name='Giveaways'),
        ),
    ]
