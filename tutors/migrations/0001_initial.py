# Generated by Django 2.0.4 on 2018-07-04 14:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('settool_common', '0006_mail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer', models.CharField(choices=[('YES', 'YES'), ('MAYBE', 'MAYBE'), ('NO', 'NO')], max_length=10, null=True, verbose_name='Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('name_de', models.CharField(max_length=250, null=True, verbose_name='Name')),
                ('name_en', models.CharField(max_length=250, null=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('description_de', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('begin', models.DateTimeField(verbose_name='Begin')),
                ('end', models.DateTimeField(verbose_name='End')),
                ('meeting_point', models.CharField(max_length=200, verbose_name='Meeting Point')),
                ('meeting_point_de', models.CharField(max_length=200, null=True, verbose_name='Meeting Point')),
                ('meeting_point_en', models.CharField(max_length=200, null=True, verbose_name='Meeting Point')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settool_common.Semester', verbose_name='Semester')),
                ('subjects', models.ManyToManyField(blank=True, to='settool_common.Subject', verbose_name='Subjects')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MailTutorTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settool_common.Mail')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=100, verbose_name='Question')),
                ('question_de', models.CharField(max_length=100, null=True, verbose_name='Question')),
                ('question_en', models.CharField(max_length=100, null=True, verbose_name='Question')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settool_common.Semester', verbose_name='Semester')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('open_registration', models.DateTimeField(verbose_name='Open registration')),
                ('close_registration', models.DateTimeField(verbose_name='Close registration')),
                ('mail_confirmed_place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutors_mail_confirmed_place', to='settool_common.Mail', verbose_name='Mail Confirmed Place')),
                ('mail_registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutors_mail_registration', to='settool_common.Mail', verbose_name='Mail Registration')),
                ('mail_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutors_mail_task', to='settool_common.Mail', verbose_name='Mail Task')),
                ('mail_waiting_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutors_mail_waiting_list', to='settool_common.Mail', verbose_name='Mail Waiting List')),
                ('semester', models.OneToOneField(on_delete=None, to='settool_common.Semester')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubjectTutorCountAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('wanted', models.IntegerField(blank=True, default=0, null=True)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settool_common.Semester')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settool_common.Subject')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, verbose_name='Task name')),
                ('name_de', models.CharField(max_length=250, null=True, verbose_name='Task name')),
                ('name_en', models.CharField(max_length=250, null=True, verbose_name='Task name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('description_de', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('begin', models.DateTimeField(verbose_name='Begin')),
                ('end', models.DateTimeField(verbose_name='End')),
                ('meeting_point', models.CharField(max_length=50, verbose_name='Meeting point')),
                ('meeting_point_de', models.CharField(max_length=50, null=True, verbose_name='Meeting point')),
                ('meeting_point_en', models.CharField(max_length=50, null=True, verbose_name='Meeting point')),
                ('min_tutors', models.IntegerField(blank=True, null=True, verbose_name='Tutors (min)')),
                ('max_tutors', models.IntegerField(blank=True, null=True, verbose_name='Tutors (max)')),
                ('allowed_subjects', models.ManyToManyField(blank=True, to='settool_common.Subject', verbose_name='Allowed Subjects')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutors.Event', verbose_name='Event')),
                ('requirements', models.ManyToManyField(blank=True, to='tutors.Question', verbose_name='Requirements')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settool_common.Semester', verbose_name='Semester')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30, verbose_name='First name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email address')),
                ('registration_time', models.DateTimeField(auto_now_add=True, verbose_name='Registration Time')),
                ('ects', models.BooleanField(default=False, help_text='tutors_ects_agreement', verbose_name='I want to receive ECTS for my work as a SET tutor.')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Birthday')),
                ('matriculation_number', models.CharField(blank=True, max_length=8, null=True, validators=[django.core.validators.RegexValidator('^[0-9]{8,8}$', message='The matriculation number has to be of the form 01234567.')], verbose_name='Matriculation number')),
                ('tshirt_size', models.CharField(choices=[('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], max_length=5, verbose_name='Tshirt size')),
                ('tshirt_girls_cut', models.BooleanField(verbose_name='Tshirt as Girls cut')),
                ('status', models.CharField(choices=[('accepted', 'accepted'), ('active', 'active'), ('declined', 'declined'), ('inactive', 'inactive')], default='inactive', max_length=100, verbose_name='Status')),
                ('comment', models.TextField(blank=True, max_length=500, verbose_name='Comment')),
                ('answers', models.ManyToManyField(blank=True, through='tutors.Answer', to='tutors.Question', verbose_name='Tutor Answers')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settool_common.Semester', verbose_name='Semester')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='settool_common.Subject', verbose_name='Subject')),
            ],
        ),
        migrations.CreateModel(
            name='TutorAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('absent', models.BooleanField(default=False, verbose_name='absent')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutors.Task')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutors.Tutor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='task',
            name='tutors',
            field=models.ManyToManyField(blank=True, through='tutors.TutorAssignment', to='tutors.Tutor', verbose_name='Assigned tutors'),
        ),
        migrations.AddField(
            model_name='mailtutortask',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tutors.Task'),
        ),
        migrations.AddField(
            model_name='mailtutortask',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutors.Tutor'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutors.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutors.Tutor'),
        ),
        migrations.AlterUniqueTogether(
            name='tutor',
            unique_together={('semester', 'email')},
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('tutor', 'question')},
        ),
    ]
