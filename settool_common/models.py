import datetime
import re

from django.core.mail import send_mail
from django.db import models
from django.http import HttpRequest
from django.template import Template
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from .settings import SEMESTER_SESSION_KEY


@deconstructible
class Semester(models.Model):
    class Meta:
        unique_together = (("semester", "year"),)
        ordering = ["year", "semester"]

    WINTER = "WS"
    SUMMER = "SS"
    SEMESTER_CHOICES = (
        (WINTER, _("Winter semester")),
        (SUMMER, _("Summer semester")),
    )

    semester = models.CharField(
        max_length=2,
        choices=SEMESTER_CHOICES,
        default=WINTER,
        verbose_name=_("Semester"),
    )

    year = models.PositiveIntegerField(
        verbose_name=_("Year"),
    )

    def __str__(self):
        return f"{self.get_semester_display()} {self.year:4}"


class Subject(models.Model):
    class Meta:
        unique_together = (("degree", "subject"),)
        ordering = ["degree", "subject"]

    BACHELOR = "BA"
    MASTER = "MA"
    DEGREE_CHOICES = (
        (BACHELOR, _("Bachelor")),
        (MASTER, _("Master")),
    )

    MATHEMATICS = "Mathe"
    PHYSICS = "Physik"
    INFORMATICS = "Info"
    GAMES_ENGINEERING = "Games"
    INFORMATION_SYSTEMS = "Winfo"
    ASE = "ASE"
    CSE = "CSE"
    BMC = "BMC"
    ROBOTICS = "Robotics"
    OPERATIONS_RESEARCH = "Mathe OR"
    SCIENCE_ENGINEERING = "Mathe SE"
    FINANCE = "Mathe Finance"
    BIOMATHE = "Mathe Bio"

    SUBJECT_CHOICES = (
        (MATHEMATICS, _("Mathematics")),
        (PHYSICS, _("Physics")),
        (INFORMATICS, _("Informatics")),
        (GAMES_ENGINEERING, _("Informatics: Games Engineering")),
        (INFORMATION_SYSTEMS, _("Information Systems")),
        (ASE, _("Automotive Software Engineering")),
        (CSE, _("Computational Science and Engineering")),
        (BMC, _("Biomedical Computing")),
        (ROBOTICS, _("Robotics, Cognition, Intelligence")),
        (OPERATIONS_RESEARCH, _("Mathematics in Operatios Research")),
        (SCIENCE_ENGINEERING, _("Mathematics in Science and Engineering")),
        (FINANCE, _("Mathematics in Finance and Acturial Science")),
        (BIOMATHE, _("Mathematics in Bioscience")),
    )

    degree = models.CharField(
        max_length=2,
        choices=DEGREE_CHOICES,
        default=BACHELOR,
        verbose_name=_("Degree"),
    )

    subject = models.CharField(
        max_length=20,
        choices=SUBJECT_CHOICES,
        default=INFORMATICS,
        verbose_name=_("Subject"),
    )

    def __str__(self):
        return f"{self.get_degree_display()} {self.get_subject_display()}"


def current_semester() -> Semester:
    now = timezone.now()
    year = now.year
    if now < timezone.make_aware(datetime.datetime(year, 5, 1)):
        semester = Semester.SUMMER
    elif now >= timezone.make_aware(datetime.datetime(year, 11, 1)):
        semester = Semester.SUMMER
        year += 1
    else:
        semester = Semester.WINTER
    return Semester.objects.get_or_create(semester=semester, year=year)[0]


def get_semester(request: HttpRequest) -> int:
    sem: int
    try:
        sem = request.session[SEMESTER_SESSION_KEY]
    except KeyError:
        sem = current_semester().pk
        request.session[SEMESTER_SESSION_KEY] = sem
    return sem  # noqa: R504


class Mail(models.Model):
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name="set_mail_set",
    )

    SET = "SET-Team <set@fs.tum.de>"
    SET_FAHRT = "SET-Fahrt-Team <setfahrt@fs.tum.de>"
    SET_TUTOR = "SET-Tutor-Team <set-tutoren@fs.tum.de>"
    SET_BAGS = "Sponsoring-Team des SET-Referats <set-tueten@fs.tum.de>"
    FROM_CHOICES = (
        (SET, _("SET")),
        (SET_FAHRT, _("SET_FAHRT")),
        (SET_TUTOR, _("SET_TUTOR")),
        (SET_BAGS, _("SET_BAGS")),
    )

    sender = models.CharField(
        max_length=100,
        choices=FROM_CHOICES,
        default=SET,
        verbose_name=_("From"),
    )

    subject = models.CharField(
        _("Email subject"),
        max_length=200,
        help_text=_("You may use placeholders for the subject."),
    )

    text = models.TextField(
        _("Text"),
        help_text=_("You may use placeholders for the text."),
    )

    def __str__(self):
        return self.subject

    def get_mail(self, context):
        subject_template = Template(self.subject)
        subject = subject_template.render(context).rstrip()

        text_template = Template(self.text)
        text = text_template.render(context)

        return subject, text, self.sender

    def send_mail(self, context, recipient):
        subject_template = Template(self.subject)
        subject = subject_template.render(context).rstrip()

        text_template = Template(self.text)
        text = text_template.render(context)

        regex = r"({{.*?}})"
        subject_matches = re.match(regex, subject, re.MULTILINE)
        text_matches = re.match(regex, text, re.MULTILINE)

        if subject_matches is not None or text_matches is not None:
            return False
        send_mail(subject, text, self.sender, [recipient], fail_silently=False)
        return True
