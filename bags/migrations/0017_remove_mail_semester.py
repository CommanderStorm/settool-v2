# Generated by Django 3.1.5 on 2021-01-24 16:49

from django.db import migrations


def subject_includes_semester(apps, _):
    Mail = apps.get_model("bags", "mail")
    for mail in Mail.objects.all():
        semester = mail.semester
        mail.subject = f"[{semester.semester}{semester.year}] {mail.subject}"[:200]
        mail.save()


class Migration(migrations.Migration):
    dependencies = [
        ("bags", "0016_auto_20201209_1909"),
    ]

    operations = [
        migrations.RunPython(subject_includes_semester),
        migrations.RemoveField(
            model_name="mail",
            name="semester",
        ),
    ]
