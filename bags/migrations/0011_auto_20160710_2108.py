# Generated by Django 1.9 on 2016-07-10 19:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bags", "0010_auto_20160622_1500"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mail",
            name="text",
            field=models.TextField(
                help_text=(
                    "You may use {{firma}} for the company name, {{anrede}} for the greeting "
                    '"Hallo Herr/Frau XYZ" and {{formale_anrede}} for the formal greeting "Sehr '
                    'geehrte/r Herr/Frau XYZ".'
                ),
                verbose_name="Text",
            ),
        ),
    ]
