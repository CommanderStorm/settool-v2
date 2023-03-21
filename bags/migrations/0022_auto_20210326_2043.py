# Generated by Django 3.1.7 on 2021-03-26 19:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bags", "0021_auto_20210326_1632"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bagsettings",
            name="bag_count",
            field=models.PositiveSmallIntegerField(default=0, verbose_name="Total amount of Bags"),
        ),
        migrations.AlterField(
            model_name="giveaway",
            name="item_count",
            field=models.PositiveSmallIntegerField(default=0, verbose_name="Item Count"),
        ),
    ]
