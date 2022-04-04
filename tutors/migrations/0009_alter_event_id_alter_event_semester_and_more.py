# Generated by Django 4.0.3 on 2022-04-01 16:07

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("settool_common", "0017_anonymisationlog_created_at_and_more"),
        ("tutors", "0008_auto_20220321_1851"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="semester",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="settool_common.semester"),
        ),
        migrations.AlterField(
            model_name="question",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="semester",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="settool_common.semester"),
        ),
        migrations.AlterField(
            model_name="task",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="semester",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="settool_common.semester"),
        ),
        migrations.AlterField(
            model_name="tutor",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="tutor",
            name="semester",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="settool_common.semester"),
        ),
    ]