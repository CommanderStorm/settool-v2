# Generated by Django 3.1.5 on 2021-01-24 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("settool_common", "0010_mail_comment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mail",
            name="semester",
        ),
    ]
