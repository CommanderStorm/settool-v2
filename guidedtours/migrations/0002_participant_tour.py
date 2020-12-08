# Generated by Django 1.9 on 2015-12-20 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guidedtours', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='tour',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='guidedtours.Tour'),
            preserve_default=False,
        ),
    ]
