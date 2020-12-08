# Generated by Django 1.9 on 2016-06-01 07:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settool_common', '0004_auto_20151220_2255'),
        ('bags', '0006_auto_20160531_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='comment',
            field=models.CharField(default='', max_length=200, verbose_name='Comment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mail',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='settool_common.Semester'),
        ),
    ]
