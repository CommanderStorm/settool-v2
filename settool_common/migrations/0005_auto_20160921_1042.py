# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-21 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settool_common', '0004_auto_20151220_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='degree',
            field=models.CharField(choices=[('BA', 'Bachelor'), ('MA', 'Master')], default='BA', max_length=2, verbose_name='Degree'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subject',
            field=models.CharField(choices=[('Mathe', 'Mathematics'), ('Physik', 'Physics'), ('Info', 'Informatics'), ('Games', 'Informatics: Games Engineering'), ('Winfo', 'Information Systems'), ('ASE', 'Automotive Software Engineering'), ('CSE', 'Computational Science and Engineering'), ('BMC', 'Biomedical Computing'), ('Robotics', 'Robotics, Cognition, Intelligence'), ('Mathe OR', 'Mathematics in Operatios Research'), ('Mathe SE', 'Mathematics in Science and Engineering'), ('Mathe Finance', 'Mathematics in Finance and Acturial Science'), ('Mathe Bio', 'Mathematics in Bioscience')], default='Info', max_length=20, verbose_name='Subject'),
        ),
    ]