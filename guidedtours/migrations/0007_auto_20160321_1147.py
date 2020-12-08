# Generated by Django 1.9 on 2016-03-21 10:47

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("guidedtours", "0006_tour_capacity"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="tour",
            options={
                "permissions": (
                    ("view_participants", "Can view and edit the list of participants"),
                ),
            },
        ),
        migrations.AlterField(
            model_name="participant",
            name="subject",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="settool_common.Subject",
                verbose_name="Subject",
            ),
        ),
        migrations.AlterField(
            model_name="participant",
            name="time",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Registration Time"),
        ),
        migrations.AlterField(
            model_name="participant",
            name="tour",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="guidedtours.Tour",
                verbose_name="Tour",
            ),
        ),
    ]
