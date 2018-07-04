# Generated by Django 2.0.4 on 2018-07-04 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settool_common', '0005_auto_20160921_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(choices=[('SET-Team <set@fs.tum.de>', 'SET'), ('SET-Fahrt-Team <setfahrt@fs.tum.de>', 'SET_FAHRT'), ('SET-Tutor-Team <settutor@fs.tum.de>', 'SET_TUTOR')], default='SET-Team <set@fs.tum.de>', max_length=100, verbose_name='From')),
                ('subject', models.CharField(help_text='You may use placeholders for the subject.', max_length=200, verbose_name='Email subject')),
                ('text', models.TextField(help_text='You may use placeholders for the text.', verbose_name='Text')),
                ('semester', models.ForeignKey(on_delete=None, related_name='set_mail_set', to='settool_common.Semester')),
            ],
        ),
    ]
