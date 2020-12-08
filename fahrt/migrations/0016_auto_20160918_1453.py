# Generated by Django 1.9 on 2016-09-18 12:53

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fahrt', '0015_auto_20160918_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='fahrt',
            name='close_registration',
            field=models.DateField(default=datetime.datetime(2016, 9, 18, 12, 52, 55, 331192, tzinfo=utc), verbose_name='Close registration'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fahrt',
            name='open_registration',
            field=models.DateField(default=datetime.datetime(2016, 9, 18, 12, 53, 5, 293845, tzinfo=utc), verbose_name='Open registration'),
            preserve_default=False,
        ),
    ]
