# Generated by Django 3.1.7 on 2021-03-21 15:11

import django.db.models.deletion
from django.db import migrations, models


def keep_giveaway_data(apps, _):
    Company = apps.get_model("bags", "company")
    Giveaway = apps.get_model("bags", "Giveaway")
    for company in Company.objects.all():
        Giveaway.objects.create(
            name=company.giveaways,
            arrival_time=company.arrival_time,
            arrived=company.arrived,
            company=company,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("settool_common", "0015_auto_20210319_2055"),
        ("bags", "0019_auto_20210217_2230"),
    ]

    operations = [
        migrations.CreateModel(
            name="GiveawayGroup",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, verbose_name="Giveaway-groups' name")),
                (
                    "semester",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="settool_common.semester"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Giveaway",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, verbose_name="Giveaway-title")),
                ("every_x_bags", models.FloatField(default=1.0, verbose_name="Insert every x bags")),
                ("per_bag_count", models.PositiveSmallIntegerField(default=1, verbose_name="Capacity per Bag")),
                ("arrival_time", models.CharField(blank=True, max_length=200, verbose_name="Arrival time")),
                ("arrived", models.BooleanField(default=False, verbose_name="Arrived")),
                ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="bags.company")),
                (
                    "group",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="bags.giveawaygroup",
                    ),
                ),
            ],
        ),
        migrations.RunPython(keep_giveaway_data),
        migrations.RemoveField(model_name="company", name="arrival_time"),
        migrations.RemoveField(model_name="company", name="arrived"),
        migrations.RemoveField(model_name="company", name="giveaways"),
        migrations.RemoveField(model_name="company", name="giveaways_last_year"),
    ]
