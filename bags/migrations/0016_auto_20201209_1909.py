# Generated by Django 3.1.4 on 2020-12-09 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bags", "0015_auto_20181005_1855"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="contact_again",
            field=models.BooleanField(null=True, verbose_name="Contact again"),
        ),
        migrations.AlterField(
            model_name="company",
            name="promise",
            field=models.BooleanField(null=True, verbose_name="Promise"),
        ),
    ]