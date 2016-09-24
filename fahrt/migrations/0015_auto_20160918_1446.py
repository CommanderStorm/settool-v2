# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-18 12:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fahrt', '0013_auto_20160917_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mylogentry_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
