import csv
import os
import time

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q, QuerySet
from django.db.models.aggregates import Count
from django.forms import formset_factory
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from settool_common import utils
from settool_common.models import get_semester, Semester
from settool_common.utils import get_or_none

from .forms import (
    CompanyForm,
    CSVFileUploadForm,
    FilterCompaniesForm,
    GiveawayDistributionModelForm,
    GiveawayForm,
    GiveawayGroupForm,
    GiveawayToGiveawayGroupForm,
    ImportForm,
    MailForm,
    SelectCompanyForm,
    SelectMailForm,
    UpdateFieldForm,
)
from .models import BagMail, Company, Giveaway, GiveawayGroup


def get_possibly_filtered_companies(filterform, semester):
    companies = semester.company_set.order_by("name")
    if filterform.is_valid():
        if filterform.cleaned_data["no_email_sent"]:
            companies = companies.filter(email_sent_success=False)
        if filterform.cleaned_data["last_year"]:
            companies = companies.filter(last_year=True)
        if filterform.cleaned_data["not_last_year"]:
            companies = companies.filter(last_year=False)
        if filterform.cleaned_data["contact_again"]:
            companies = companies.filter(contact_again=True)
        if filterform.cleaned_data["promise"]:
            companies = companies.filter(promise=True)
        if filterform.cleaned_data["no_promise"]:
            companies = companies.exclude(promise=True)
        if filterform.cleaned_data["giveaways"]:
            companies = companies.exclude(giveaway__isnull=True)
        if filterform.cleaned_data["no_giveaway"]:
            companies = companies.filter(giveaway__isnull=True)
        if filterform.cleaned_data["arrived"]:
            companies = companies.filter(giveaway__arrived=True)
    return companies  # noqa: R504


@permission_required("bags.view_companies")
def list_companys(request: WSGIRequest) -> HttpResponse:
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    filterform = FilterCompaniesForm(request.POST or None)
    companies = get_possibly_filtered_companies(filterform, semester)

    mailform = SelectMailForm(request.POST if "mailform" in request.POST else None)
    select_company_form_set = formset_factory(SelectCompanyForm, extra=0)
    companyforms = select_company_form_set(
        request.POST if "mailform" in request.POST else None,
        initial=[{"id": c.id, "selected": True} for c in companies],
    )

    if "mailform" in request.POST and mailform.is_valid() and companyforms.is_valid():
        mail = mailform.cleaned_data["mail"]

        selected_companies = []
        for company in companyforms:
            try:
                company_id = company.cleaned_data["id"]
            except KeyError:
                continue
            try:
                selected = company.cleaned_data["selected"]
            except KeyError:
                selected = False
            if selected:
                selected_companies.append(company_id)

        request.session["selected_companies"] = selected_companies
        return redirect("bags:send_mail", mail.id)

    companies_and_select = []
    for company in companies:
        for company_form in companyforms:
            if company_form.initial["id"] == company.id:
                companies_and_select.append((company, company_form))
                break

    context = {
        "companies_and_select": companies_and_select,
        "filterform": filterform,
        "mailform": mailform,
        "companyforms": companyforms,
    }
    return render(request, "bags/company/list_companys.html", context)


@permission_required("bags.view_companies")
def add_company(request: WSGIRequest) -> HttpResponse:
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))

    form = CompanyForm(request.POST or None, semester=semester)
    if form.is_valid():
        company = form.save()

        return redirect("bags:view_company", company.id)

    context = {"form": form}
    return render(request, "bags/company/add_company.html", context)


@permission_required("bags.view_companies")
def view_company(request: WSGIRequest, company_pk: int) -> HttpResponse:
    company = get_object_or_404(Company, pk=company_pk)

    context = {"company": company}
    return render(request, "bags/company/view_company.html", context)


@permission_required("bags.view_companies")
def edit_company(request: WSGIRequest, company_pk: int) -> HttpResponse:
    company = get_object_or_404(Company, pk=company_pk)

    form = CompanyForm(
        request.POST or None,
        semester=company.semester,
        instance=company,
    )
    if form.is_valid():
        form.save()

        return redirect("bags:view_company", company.id)

    context = {
        "form": form,
        "company": company,
    }
    return render(request, "bags/company/edit_company.html", context)


@permission_required("bags.view_companies")
def update_field(request: WSGIRequest, company_pk: int, field: str) -> HttpResponse:
    company = get_object_or_404(Company, pk=company_pk)

    form = UpdateFieldForm(request.POST or None)
    if form.is_valid():
        private_key = form.cleaned_data["pk"]
        name = form.cleaned_data["name"]
        value = form.cleaned_data["value"]
        if private_key != company.pk or name != f"company_{company.pk}_{field}":
            return HttpResponseBadRequest("")
        str_to_bool_map = {
            "True": True,
            "False": False,
            "None": None,
        }
        if value in str_to_bool_map:
            value = str_to_bool_map.get(value)
        changes = {field: value}

        # to display email_sent_success and email_sent_success in one column we use a Failure state
        # email_sent_success is apparently only a failure marker if email_sent is True
        # (email_sent_success is initialised as False)
        if field == "email_sent":
            if value == "Failure":
                changes["email_sent"] = True
                changes["email_sent_success"] = False
            else:
                changes["email_sent"] = changes["email_sent_success"] = value

        Company.objects.filter(pk=company.pk).update(**changes)
        return HttpResponse(f"#{name}")

    return HttpResponseBadRequest("")


@permission_required("bags.view_companies")
def del_company(request: WSGIRequest, company_pk: int) -> HttpResponse:
    company = get_object_or_404(Company, pk=company_pk)

    form = forms.Form(request.POST or None)
    if form.is_valid():
        company.delete()

        return redirect("bags:dashboard")

    context = {
        "company": company,
        "form": form,
    }
    return render(request, "bags/company/del_company.html", context)


@permission_required("bags.view_companies")
def list_mails(request: WSGIRequest) -> HttpResponse:
    context = {"mails": BagMail.objects.all()}
    return render(request, "bags/mail/list_mails.html", context)


@permission_required("bags.view_companies")
def add_mail(request: WSGIRequest) -> HttpResponse:
    form = MailForm(request.POST or None)
    if form.is_valid():
        form.save()

        return redirect("bags:list_mails")

    context = {"form": form, "mail": BagMail}
    return render(request, "bags/mail/add_mail.html", context)


@permission_required("bags.view_companies")
def edit_mail(request: WSGIRequest, mail_pk: int) -> HttpResponse:
    mail = get_object_or_404(BagMail, pk=mail_pk)

    form = MailForm(request.POST or None, instance=mail)
    if form.is_valid():
        form.save()
        return redirect("bags:list_mails")

    context = {
        "form": form,
        "mail": mail,
    }
    return render(request, "bags/mail/edit_mail.html", context)


@permission_required("bags.view_companies")
def delete_mail(request: WSGIRequest, mail_pk: int) -> HttpResponse:
    mail = get_object_or_404(BagMail, pk=mail_pk)

    form = forms.Form(request.POST or None)
    if form.is_valid():
        mail.delete()

        return redirect("bags:list_mails")

    context = {
        "mail": mail,
        "form": form,
    }
    return render(request, "bags/mail/del_mail.html", context)


@permission_required("bags.view_companies")
def send_mail(request: WSGIRequest, mail_pk: int) -> HttpResponse:
    mail = get_object_or_404(BagMail, pk=mail_pk)
    selected_companies = request.session["selected_companies"]
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    companies = semester.company_set.filter(
        id__in=selected_companies,
    ).order_by("name")

    subject, text, from_email = mail.get_mail_company()

    form = forms.Form(request.POST or None)
    if form.is_valid():
        company: Company
        for company in companies:
            company.email_sent_success = mail.send_mail_company(company)
            company.email_sent = True
            company.save()
        return redirect("bags:dashboard")

    context = {
        "companies": companies,
        "subject": subject,
        "text": text,
        "from_email": from_email,
        "form": form,
    }

    return render(request, "bags/mail/send_mail.html", context)


def import_mail_csv_to_db(csv_file, semester):
    # load content into tempfile
    tmp_filename = f"upload_{csv_file.name}"
    with open(tmp_filename, "wb+") as tmp_csv_file:
        for chunk in csv_file.chunks():
            tmp_csv_file.write(chunk)
    # create new mail
    with open(tmp_filename, "r") as tmp_csv_file:
        rows = csv.DictReader(tmp_csv_file)
        for row in rows:
            Company.objects.update_or_create(
                semester=semester,
                name=row["name"],
                defaults={
                    "contact_firstname": row["contact_firstname"],
                    "contact_lastname": row["contact_lastname"],
                    "email": row["email"],
                    "contact_gender": row["contact_gender"],
                    "email_sent": row["email_sent"],
                    "email_sent_success": row["email_sent_success"],
                    "promise": row["promise"],
                    "giveaways": row["giveaways"],
                    "giveaways_last_year": row["giveaways_last_year"],
                    "arrival_time": row["arrival_time"],
                    "comment": row["comment"],
                    "last_year": row["last_year"],
                    "arrived": row["arrived"],
                    "contact_again": row["contact_again"],
                },
            )
    # delete tempfile
    os.remove(tmp_filename)


@user_passes_test(lambda user: user.is_staff)
@permission_required("bags.view_companies")
def import_csv(request: WSGIRequest) -> HttpResponse:
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    file_upload_form = CSVFileUploadForm(request.POST or None, request.FILES)
    if file_upload_form.is_valid():
        import_mail_csv_to_db(request.FILES["file"], semester)
        messages.success(request, _("The File was successfully uploaded"))
        return redirect("bags:main_index")
    return render(
        request,
        "bags/import-export/import_csv.html",
        {"form": file_upload_form},
    )


@permission_required("bags.view_companies")
@user_passes_test(lambda user: user.is_staff)
def import_previous_semester(request: WSGIRequest) -> HttpResponse:
    new_semester: Semester = get_object_or_404(Semester, pk=get_semester(request))

    form = ImportForm(request.POST or None, semester=new_semester)
    if form.is_valid():
        old_semester = form.cleaned_data["semester"]
        only_contact_again = form.cleaned_data["only_contact_again"]

        companies = old_semester.company_set.exclude(contact_again=False)
        if only_contact_again:
            companies = old_semester.company_set.filter(contact_again=True)

        for company in companies:
            # do not import company when it already exists
            if new_semester.company_set.filter(name=company.name).exists():
                continue

            Company.objects.create(
                semester=new_semester,
                name=company.name,
                contact_gender=company.contact_gender,
                contact_firstname=company.contact_firstname,
                contact_lastname=company.contact_lastname,
                email=company.email,
                email_sent=False,
                email_sent_success=False,
                promise=None,
                comment="",
                last_year=True,
                contact_again=None,
            )
        return redirect("bags:dashboard")

    context = {
        "form": form,
    }

    return render(request, "bags/import-export/import_companies.html", context)


@permission_required("guidedtours.view_participants")
def export_csv(request: WSGIRequest) -> HttpResponse:
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    companies = semester.company_set.order_by("name")
    return utils.download_csv(
        [
            "name",
            "contact_gender",
            "contact_firstname",
            "contact_lastname",
            "email",
            "email_sent",
            "email_sent_success",
            "promise",
            "comment",
            "last_year",
            "contact_again",
        ],
        f"companies_{time.strftime('%Y%m%d-%H%M')}.csv",
        companies,
    )


@permission_required("bags.view_companies")
def dashboard(request: WSGIRequest) -> HttpResponse:
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))

    companies: QuerySet[Company] = Company.objects.filter(semester=semester)
    g_companies: QuerySet[Company] = Company.objects.filter(giveaway__isnull=False, semester=semester)
    giveaways: QuerySet[Giveaway] = Giveaway.objects.filter(company__semester=semester)

    g_by_group = list(giveaways.filter(group__isnull=False).values("group").annotate(group_count=Count("group")))
    g_by_group.append(
        {
            "group": None,
            "group_count": giveaways.filter(group__isnull=True).count(),
        },
    )
    g_by_every_x_bags = (
        giveaways.values("every_x_bags").annotate(every_x_bags_count=Count("every_x_bags")).order_by("every_x_bags")
    )
    g_by_per_bag_count = (
        giveaways.values("per_bag_count").annotate(per_bag_count_count=Count("per_bag_count")).order_by("per_bag_count")
    )

    context = {
        "c_by_giveaway_data": [
            companies.filter(giveaway__isnull=False).count(),
            companies.filter(giveaway__isnull=True).count(),
        ],
        "c_by_contact_again_data": [
            companies.filter(contact_again=True).count(),
            companies.filter(contact_again=False).count(),
        ],
        "c_by_last_year_data": [
            companies.filter(last_year=True).count(),
            companies.filter(last_year=False).count(),
        ],
        "c_by_promise_data": [
            companies.filter(promise=True).count(),
            companies.filter(promise=False).count(),
        ],
        "c_by_email_sent_data": [
            companies.filter(email_sent=True, email_sent_success=False).count(),
            companies.filter(email_sent=True, email_sent_success=True).count(),
            companies.filter(email_sent=False).count(),
        ],
        "gc_by_contact_again_data": [
            g_companies.filter(contact_again=True).count(),
            g_companies.filter(contact_again=False).count(),
        ],
        "gc_by_last_year_data": [
            g_companies.filter(last_year=True).count(),
            g_companies.filter(last_year=False).count(),
        ],
        "gc_by_promise_data": [
            g_companies.filter(promise=True).count(),
            g_companies.filter(promise=False).count(),
        ],
        "gc_by_email_sent_data": [
            g_companies.filter(email_sent=True, email_sent_success=False).count(),
            g_companies.filter(email_sent=True, email_sent_success=True).count(),
            g_companies.filter(email_sent=False).count(),
        ],
        "gc_by_giveaway_arrived_data": [
            g_companies.filter(giveaway__arrived=True).count(),
            g_companies.filter(giveaway__arrived=False).count(),
        ],
        "g_by_group_labels": [
            str(get_or_none(GiveawayGroup, id=group["group"]) or _("NOT assigned to a giveaway-group"))
            for group in g_by_group
        ],
        "g_by_group_data": [group["group_count"] for group in g_by_group],
        "g_by_every_x_bags_labels": [str(every_x_bags["every_x_bags"]) for every_x_bags in g_by_every_x_bags],
        "g_by_every_x_bags_data": [every_x_bags["every_x_bags_count"] for every_x_bags in g_by_every_x_bags],
        "g_by_per_bag_count_labels": [str(per_bag_count["per_bag_count"]) for per_bag_count in g_by_per_bag_count],
        "g_by_per_bag_count_data": [per_bag_count["per_bag_count_count"] for per_bag_count in g_by_per_bag_count],
    }
    return render(request, "bags/bags_dashboard.html", context=context)


@permission_required("bags.view_companies")
def list_grouped_giveaways(request: WSGIRequest) -> HttpResponse:
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    context = {
        "giveaway_groups": [
            (ggroup, ggroup.giveaway_set.filter(company__semester=semester).all())
            for ggroup in semester.giveawaygroup_set.all()
        ],
        "ungrouped_giveaways": Giveaway.objects.filter(Q(group=None) & Q(company__semester=semester)),
    }
    return render(request, "bags/giveaways/giveaway/list_grouped_giveaways.html", context=context)


@permission_required("bags.view_companies")
def list_giveaways(request: WSGIRequest) -> HttpResponse:
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    context = {
        "giveaways": Giveaway.objects.filter(company__semester=semester),
    }
    return render(request, "bags/giveaways/giveaway/list_giveaways.html", context=context)


@permission_required("bags.view_companies")
def add_giveaway(request: WSGIRequest) -> HttpResponse:
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    form = GiveawayForm(request.POST or None, semester=semester)
    if form.is_valid():
        form.save()
        return redirect("bags:list_giveaways")

    context = {
        "form": form,
    }
    return render(request, "bags/giveaways/giveaway/add_giveaway.html", context=context)


class GiveawayCreateView(BSModalCreateView):
    template_name = "bags/giveaways/giveaway/update_giveaway.html"
    form_class = GiveawayDistributionModelForm
    success_message = "Success: giveaway was created."
    success_url = reverse_lazy("bags:main_index")


@permission_required("bags.view_companies")
def edit_giveaway(request: WSGIRequest, giveaway_pk: int) -> HttpResponse:
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    giveaway: Giveaway = get_object_or_404(Giveaway, id=giveaway_pk)

    form = GiveawayForm(request.POST or None, initial=giveaway, semester=semester)
    if form.is_valid():
        form.save()
        return redirect("bags:list_giveaways")

    context = {
        "giveaway": giveaway,
        "form": form,
    }
    return render(request, "bags/giveaways/giveaway/edit_giveaway.html", context=context)


class GiveawayDistributionUpdateView(BSModalUpdateView):
    model = Giveaway
    template_name = "bags/giveaways/giveaway/update_giveaway.html"
    form_class = GiveawayDistributionModelForm
    success_message = "Success: Giveaway was updated."
    success_url = reverse_lazy("bags:list_grouped_giveaways")


@permission_required("bags.view_companies")
def giveaway_data_ungrouped(request):
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    if request.method == "GET":
        ungrouped_giveaways = Giveaway.objects.filter(Q(group=None) & Q(company__semester=semester))
        data = {
            "giveaway_data_ungrouped": render_to_string(
                "bags/giveaways/giveaway/_ungrouped_giveaways.html",
                {"ungrouped_giveaways": ungrouped_giveaways},
                request=request,
            ),
        }
        return JsonResponse(data)
    raise Http404()


@permission_required("bags.view_companies")
def giveaway_data_grouped(request):
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    if request.method == "GET":
        giveaway_groups = [
            (ggroup, ggroup.giveaway_set.filter(company__semester=semester).all())
            for ggroup in semester.giveawaygroup_set.all()
        ]
        data = {
            "giveaway_data_grouped": render_to_string(
                "bags/giveaways/giveaway/_grouped_giveaways.html",
                {"giveaway_groups": giveaway_groups},
                request=request,
            ),
        }
        return JsonResponse(data)
    raise Http404()


@permission_required("bags.view_companies")
def view_giveaway(request: WSGIRequest, giveaway_pk: int) -> HttpResponse:
    giveaway: Giveaway = get_object_or_404(Giveaway, id=giveaway_pk)
    context = {
        "giveaway": giveaway,
    }
    return render(request, "bags/giveaways/giveaway/view_giveaway.html", context=context)


@permission_required("bags.view_companies")
def del_giveaway(request: WSGIRequest, giveaway_pk: int) -> HttpResponse:
    giveaway: Giveaway = get_object_or_404(Giveaway, id=giveaway_pk)

    form = forms.Form(request.POST or None)
    if form.is_valid():
        giveaway.delete()
        return redirect("bags:list_giveaways")

    context = {
        "giveaway": giveaway,
        "form": form,
    }
    return render(request, "bags/giveaways/giveaway/del_giveaway.html", context=context)


@permission_required("bags.view_companies")
def add_giveaway_group(request: WSGIRequest) -> HttpResponse:
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    form = GiveawayGroupForm(request.POST or None, semester=semester)
    if form.is_valid():
        form.save()
        return redirect("bags:list_giveaways")

    context = {
        "form": form,
    }
    return render(request, "bags/giveaways/giveaway_group/add_giveaway_group.html", context)


@permission_required("bags.view_companies")
def add_giveaway_to_giveaway_group(request: WSGIRequest, giveaway_group_pk: int) -> HttpResponse:
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    giveaway_group: GiveawayGroup = get_object_or_404(GiveawayGroup, id=giveaway_group_pk)
    form = GiveawayToGiveawayGroupForm(request.POST or None, semester=semester, giveaway_group=giveaway_group)
    if form.is_valid():
        giveaway = form.cleaned_data["giveaway"]
        giveaway.group = giveaway_group
        giveaway.save()
        return redirect("bags:list_giveaways")

    context = {
        "giveaway_group": giveaway_group,
        "form": form,
    }
    return render(request, "bags/giveaways/giveaway_group/add_giveaway_to_giveaway_group.html", context)


@permission_required("bags.view_companies")
def edit_giveaway_group(request: WSGIRequest, giveaway_group_pk: int) -> HttpResponse:
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    giveaway_group: GiveawayGroup = get_object_or_404(GiveawayGroup, id=giveaway_group_pk)

    form = GiveawayGroupForm(request.POST or None, initial=giveaway_group, semester=semester)
    if form.is_valid():
        form.save()
        return redirect("bags:list_giveaways")

    context = {
        "giveaway_group": giveaway_group,
        "form": form,
    }
    return render(request, "bags/giveaways/giveaway_group/edit_giveaway_group.html", context)


@permission_required("bags.view_companies")
def del_giveaway_group(request: WSGIRequest, giveaway_group_pk: int) -> HttpResponse:
    giveaway_group: GiveawayGroup = get_object_or_404(GiveawayGroup, id=giveaway_group_pk)

    form = forms.Form(request.POST or None)
    if form.is_valid():
        giveaway_group.delete()
        return redirect("bags:list_giveaways")

    context = {
        "giveaway_group": giveaway_group,
        "form": form,
    }
    return render(request, "bags/giveaways/giveaway_group/del_giveaway_group.html", context)


@permission_required("bags.view_companies")
def list_giveaway_group(request):
    semester: Semester = get_object_or_404(Semester, pk=get_semester(request))
    context = {
        "giveaway_groups": semester.giveawaygroup_set.all(),
    }
    return render(request, "bags/giveaways/giveaway_group/list_giveaways_group.html", context=context)
