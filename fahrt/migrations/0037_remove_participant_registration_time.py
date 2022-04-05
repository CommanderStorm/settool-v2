# Generated by Django 4.0.3 on 2022-04-05 15:39

from django.db import migrations


def migrate_participant_registration_time_created_at(apps, schema_editor):
    Participant = apps.get_model("fahrt", "Participant")
    for participant in Participant.objects.all():
        participant.created_at = participant.registration_time
        participant.save(update_fields=["created_at"])


class Migration(migrations.Migration):

    dependencies = [
        ("fahrt", "0036_remove_logentry_time"),
    ]

    operations = [
        migrations.RunPython(migrate_participant_registration_time_created_at),
        migrations.RemoveField(model_name="participant", name="registration_time"),
    ]
