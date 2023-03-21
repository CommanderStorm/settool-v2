# Generated by Django 4.0.4 on 2022-04-30 23:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("settool_common", "0018_alter_anonymisationlog_semester"),
        ("fahrt", "0034_remove_participant_id_alter_logentry_participant_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="participant",
            name="semester",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="settool_common.semester",
                verbose_name="Semester",
            ),
        ),
    ]
