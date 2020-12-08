# Generated by Django 1.9 on 2016-05-31 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bags', '0003_auto_20160531_1111'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'permissions': (('view_companies', 'Can view and edit the companies'),)},
        ),
        migrations.RemoveField(
            model_name='company',
            name='zusage',
        ),
        migrations.AddField(
            model_name='company',
            name='promise',
            field=models.NullBooleanField(verbose_name='Promise'),
        ),
    ]
