from __future__ import unicode_literals
import uuid

from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from settool_common.models import Semester, Subject
from settool_common.utils import u


class Status(models.Model):
    name = models.CharField(
        _("Status name"),
        max_length = 30,
    )

    default_status = models.BooleanField(
        _("Default status"),
    )

    def __str__(self):
        return u(self.name)


def get_default_status():
    default = Status.objects.filter(default_status=True).order_by('pk').first()
    if default:
        return default.pk
    else:
        return 1


class Tutor(models.Model):
    TSHIRT_SIZES = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL')
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    semester = models.OneToOneField(
        Semester,
        verbose_name=_("Semester"),
        on_delete=models.CASCADE,
    )

    first_name = models.CharField(
        _("First name"),
        max_length=30,
    )

    last_name = models.CharField(
        _("Last name"),
        max_length=50,
    )

    email = models.EmailField(
        _("Email address"),
    )

    registration_time = models.DateTimeField(
        _("Registration Time"),
        auto_now_add=True,
    )

    birthday = models.DateField(
        _("Birthday"),
    )

    matriculation_number = models.CharField(
        _("Matriculation number"),
        max_length=8,
        validators=[RegexValidator(
            r'^[0-9]{8,8}$',
            message=_('The matriculation number has to be of the form ' \
                '01234567.'),
        )],
    )

    tshirt_size = models.CharField(
        _("Tshirt size"),
        max_length=5,
        choices=TSHIRT_SIZES,
    )

    tshirt_girls_cut = models.BooleanField(
        _("Tshirt as Girls cut"),
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.SET_DEFAULT,
        verbose_name=_("Status"),
        default=get_default_status,
    )

    subject = models.ForeignKey(
        Subject,
        verbose_name=_("Subject"),
        on_delete=models.CASCADE,
    )

    minor_subject = models.CharField(
        _("Minor subject"),
        max_length=30,
    )

    def __str__(self):
        return "{0} {1}".format(u(self.first_name), u(self.last_name))


class Task(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    semester = models.OneToOneField(
        Semester,
        verbose_name=_("Semester"),
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        _("Task name"),
        max_length=50,
    )

    begin = models.DateTimeField(
        _("Begin"),
    )

    end = models.DateTimeField(
        _("End"),
    )

    description = models.TextField(
        _("Description"),
    )

    meeting_point = models.CharField(
        _("Meeting point"),
        max_length=50,
    )

    prevented_tutors = models.ManyToManyField(
        Tutor,
        verbose_name=_("Prevented Tutors"),
        blank=True,
    )

    task_requirements = models.ManyToManyField(
        'Question',
        verbose_name=_("Task requirements"),
        through="Requirement",
        blank=True,
    )

    def __str__(self):
        return u(self.name)


class Group(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    task = models.ForeignKey(
        Task,
        verbose_name=_("Task"),
        on_delete=models.CASCADE,
    )

    number = models.CharField(
        _("Group number"),
        max_length=20,
    )

    required_tutors = models.IntegerField(
        _("Number of required tutors"),
    )

    subjects = models.ManyToManyField(
        Subject,
        verbose_name=_("Allowed subjects"),
        blank=True,
    )

    tutors = models.ManyToManyField(
        Tutor,
        verbose_name=_("Assigned tutors"),
        through='TutorAssignment', 
        blank=True,
    )

    def __str__(self):
        return "{} - {}".format(self.task, u(self.number))


class TutorAssignment(models.Model):
    tutor = models.ForeignKey(
        Tutor,
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )

    absent = models.BooleanField(
        _("absent"),
        default=False,
    )

    def __str__(self):
        return "{} @ {}".format(self.tutor, self.group)


class Question(models.Model):
    question = models.CharField(
        _("Question"),
        max_length=100,
    )

    tutor_answers = models.ManyToManyField(
        Tutor,
        verbose_name=_("Assigned tutors"),
        through='Answer',
        blank=True,
    )

    def __str__(self):
        return u(self.question)


class Answer(models.Model):
    YES = 'YES'
    NO = 'NO'
    MAYBE = 'MAYBE'
    ANSWERS = (
        (YES, _("yes")),
        (MAYBE, _("if need be")),
        (NO, _("no")),
    )

    tutor = models.ForeignKey(
        Tutor,
        on_delete=models.CASCADE,
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )

    answer = models.CharField(
        _("Answer"),
        max_length=10,
        blank=True,
        choices=ANSWERS,
    )

    def __str__(self):
        return "{}: {} -> {}".format(self.tutor, self.question, u(self.answer))


class Requirement(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )

    inverse = models.BooleanField(
        _("inverse answer"),
    )

    def __str__(self):
        return "{}: {}".format(self.task, self.question)
