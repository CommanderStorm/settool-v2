# Generated by Django 3.1.6 on 2021-02-18 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("settool_common", "0011_remove_mail_semester"),
        ("fahrt", "0027_auto_20210216_0111"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transportation",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "transport_type",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Car"), (1, "Train")],
                        verbose_name="Type of Transport",
                    ),
                ),
                (
                    "places",
                    models.PositiveSmallIntegerField(
                        default=1,
                        verbose_name="Number of people (totally) for this mode of transport",
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="participant",
            name="car",
        ),
        migrations.RemoveField(
            model_name="participant",
            name="car_places",
        ),
        migrations.CreateModel(
            name="TransportationComment",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("comment_content", models.CharField(max_length=200, verbose_name="Text")),
                (
                    "commented_on",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="fahrt.transportation"),
                ),
                ("sender", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="fahrt.participant")),
            ],
        ),
        migrations.AddField(
            model_name="transportation",
            name="creator",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="fahrt_transportation_creator",
                to="fahrt.participant",
            ),
        ),
        migrations.AddField(
            model_name="transportation",
            name="fahrt",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fahrt_transportation",
                to="settool_common.semester",
            ),
        ),
        migrations.AddField(
            model_name="participant",
            name="transportation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="fahrt.transportation",
            ),
        ),
    ]
