# Generated by Django 1.9 on 2015-12-20 16:08

from typing import List, Tuple

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies: List[Tuple[str, str]] = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=200, verbose_name='First name')),
                ('surname', models.CharField(max_length=200, verbose_name='Surname')),
                ('email', models.EmailField(max_length=254, verbose_name='E-Mail')),
                ('phone', models.CharField(max_length=200, verbose_name='Mobile phone')),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('date', models.DateTimeField(verbose_name='Date')),
            ],
        ),
    ]
