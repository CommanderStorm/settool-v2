# Generated by Django 1.9 on 2016-06-22 13:00

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bags", "0009_auto_20160608_1218"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mail",
            name="comment",
            field=models.CharField(
                blank=True,
                max_length=200,
                verbose_name="Comment",
            ),
        ),
    ]
