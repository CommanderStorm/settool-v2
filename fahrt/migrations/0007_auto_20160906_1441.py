# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-06 12:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fahrt', '0006_auto_20160906_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='mailinglist',
            field=models.BooleanField(default=False, verbose_name='Mailing list'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='status',
            field=models.CharField(choices=[('registered', 'registered'), ('confirmed', 'confirmed'), ('cancelled', 'cancelled')], default='registered', max_length=200, verbose_name='Status'),
        ),
    ]