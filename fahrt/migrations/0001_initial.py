# Generated by Django 1.9 on 2016-09-06 12:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("settool_common", "0004_auto_20151220_2255"),
    ]

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("male", "male"),
                            ("female", "female"),
                        ],
                        max_length=200,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "firstname",
                    models.CharField(
                        max_length=200,
                        verbose_name="First name",
                    ),
                ),
                (
                    "surname",
                    models.CharField(
                        max_length=200,
                        verbose_name="Surname",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        verbose_name="Email address",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        verbose_name="Phone",
                    ),
                ),
                (
                    "mobile",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        verbose_name="Mobile phone",
                    ),
                ),
                (
                    "nutrition",
                    models.CharField(
                        choices=[
                            ("normal", "normal"),
                            ("vegeterian", "vegeterian"),
                            ("vegan", "vegan"),
                        ],
                        max_length=200,
                        verbose_name="Nutrition",
                    ),
                ),
                (
                    "allergies",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        verbose_name="Allergies",
                    ),
                ),
                (
                    "car",
                    models.BooleanField(
                        verbose_name="Drive by car",
                    ),
                ),
                (
                    "car_places",
                    models.IntegerField(
                        blank=True,
                        verbose_name="Places in my car",
                    ),
                ),
                (
                    "non_liability",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="Non-liability submitted",
                    ),
                ),
                (
                    "paid",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="Paid",
                    ),
                ),
                (
                    "payment_deadline",
                    models.DateTimeField(
                        blank=True,
                        verbose_name="Payment deadline",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("registered", "registered"),
                            ("confirmed", "confirmed"),
                            ("cancelled", "cancelled"),
                        ],
                        max_length=200,
                        verbose_name="Status",
                    ),
                ),
                (
                    "mailinglist",
                    models.BooleanField(
                        verbose_name="Mailing list",
                    ),
                ),
                (
                    "comment",
                    models.CharField(
                        max_length=400,
                        verbose_name="Comment",
                    ),
                ),
                (
                    "time",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Registration time",
                    ),
                ),
                (
                    "semester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="settool_common.Semester",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="settool_common.Subject",
                        verbose_name="Subject",
                    ),
                ),
            ],
        ),
    ]
