# Generated by Django 4.0.3 on 2022-03-21 18:13

from django.db import migrations

import settool_common.models


def migrate_mail_tourmail(apps, _):
    Mail = apps.get_model("settool_common", "Mail")
    TourMail = apps.get_model("guidedtours", "TourMail")
    for mail in Mail.objects.filter(sender=settool_common.models.Mail.SET):
        TourMail.objects.create(
            sender=settool_common.models.Mail.SET,
            subject=mail.subject,
            text=mail.text,
            comment=mail.comment,
        )
        mail.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("settool_common", "0016_alter_coursebundle_options_alter_subject_options_and_more"),
        ("guidedtours", "0018_tour_length"),
    ]

    operations = [
        migrations.RunPython(migrate_mail_tourmail),
    ]
