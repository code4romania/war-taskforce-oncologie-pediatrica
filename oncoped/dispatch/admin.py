from django.conf import settings
from django.contrib import admin
from django.db.models import Sum, TextField
from django.forms import ModelForm, Textarea
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportModelAdmin

from dispatch.models import (
    Clinic,
    Companion,
    LogisticAndSocialAssistance,
    MedicalAssistance,
    PatientRequest,
    PatientRequestFile,
)

admin.site.index_template = "admin/custom_admin_index.html"


def admin_index_custom_context(request):
    ctx = {}
    if request.path[3:] == "/admin/":
        patients_count_all = PatientRequest.objects.count()
        patients_assigned = PatientRequest.objects.filter(med_assistance__clinic__isnull=False).count()
        patiens_unassigned = patients_count_all - patients_assigned

        ctx["count_patient_requests_all"] = patients_count_all
        ctx["count_patient_requests_assigned"] = patients_assigned
        ctx["count_patient_requests_unassigned"] = patiens_unassigned
        try:
            if patients_assigned:
                if patiens_unassigned:
                    ctx["patient_requests_assigned_percentage"] = int(
                        round((1 - (patiens_unassigned / patients_count_all)) * 100, 0)
                    )
                else:
                    ctx["patient_requests_assigned_percentage"] = 100
            else:
                ctx["patient_requests_assigned_percentage"] = 0
        except ZeroDivisionError:
            ctx["patient_requests_assigned_percentage"] = 0

        clinics_count = Clinic.objects.count()
        all_beds = (
            Clinic.objects.annotate(all_beds=Sum("available_beds")).values_list("all_beds", flat=True).first()
        ) or 0
        available_beds = all_beds - patients_assigned
        try:
            if all_beds:
                beds_occupation = int(round((1 - (available_beds / all_beds)) * 100, 0))
            else:
                beds_occupation = 100
        except ZeroDivisionError:
            beds_occupation = 0

        ctx["count_clinics"] = clinics_count
        ctx["count_clinics_all_beds"] = all_beds
        ctx["count_clinics_available_beds"] = available_beds
        ctx["count_clinics_beds_occupation"] = beds_occupation

    return ctx


class PatientRequestFileInLine(admin.TabularInline):
    model = PatientRequestFile
    extra = 1
    verbose_name_plural = _("Upload Medical Files")


@admin.register(PatientRequestFile)
class AdminPatientRequestFile(admin.ModelAdmin):
    # Just to hide the model in admin...
    def get_model_perms(self, request):
        return {}


class MedicalAssistanceInLine(admin.StackedInline):
    model = MedicalAssistance

    verbose_name = _("Add Medical Assitance")
    verbose_name_plural = _("Add Medical Assitance")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'clinic':
            kwargs['queryset'] = Clinic.objects.exclude(available_beds__lte=0)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MedicalAssistance)
class AdminMedicalAssistance(admin.ModelAdmin):
    # Just to hide the model in admin...
    def get_model_perms(self, request):
        return {}


class LogisticAndSocialAssistanceInLine(admin.StackedInline):
    model = LogisticAndSocialAssistance

    verbose_name = _("Add Logistic & Social Assistance")
    verbose_name_plural = _("Add Logistic & Social Assistance")

    fieldsets = (
        (
            _("Transport"),
            {
                "fields": (
                    "transport_required",
                    "transport_status",
                    "transport",
                    "pick_up_location",
                    "destination_location",
                    "transport_details",
                    "transport_rep_external",
                    "transport_rep_external_details",
                ),
                "classes": ("my-section",),
            },
        ),
        (
            _("Accommodation"),
            {
                "fields": (
                    "accommodation_required",
                    "accommodation_status",
                    "accommodation_details",
                    "accommodation_rep_external",
                    "accommodation_rep_external_details",
                ),
            },
        ),
        (
            _("Assistance"),
            {
                "fields": (
                    "assistance_required",
                    "assistance_status",
                    "assistance_rep_external",
                    "assistance_rep_external_details",
                ),
            },
        ),
    )


@admin.register(LogisticAndSocialAssistance)
class AdminLogisticAndSocialAssistance(admin.ModelAdmin):
    # Just to hide the model in admin...
    def get_model_perms(self, request):
        return {}


class CompanionInLine(admin.StackedInline):
    model = Companion
    extra = 1
    max_num = 5
    verbose_name = _("Add Companion")
    verbose_name_plural = _("Add Companion")


@admin.register(Companion)
class AdminCompanion(admin.ModelAdmin):
    # Just to hide the model in admin...
    def get_model_perms(self, request):
        return {}


@admin.register(Clinic)
class AdminClinic(ImportExportModelAdmin):

    list_per_page = settings.LIST_PER_PAGE

    list_display = [
        "tumor_type",
        "name",
        "city",
        "county",
        "address",
        "hospitalization_office_email",
        "hospitalization_office_phone_number",
        "head_of_dept_name",
        "head_of_dept_email",
        "dept_phone",
        "available_beds",
    ]

    list_display_links = [
        "tumor_type",
        "name",
    ]

    search_fields = [
        "tumor_type",
        "name",
        "city",
        "county",
    ]

    list_filter = [
        "tumor_type",
        "therapy_services",
        "name",
        "city",
        "county",
    ]

    ordering = ("pk",)

    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 63})},
    }


class AdminPatientRequestForm(ModelForm):
    model = PatientRequest

    class Meta:
        help_texts = {
            "get_child_age": _("Age will be computed once the form is saved."),
        }


@admin.register(PatientRequest)
class AdminPatientRequest(ImportExportModelAdmin):
    form = AdminPatientRequestForm

    list_per_page = settings.LIST_PER_PAGE

    def assigned_clinic(self, obj):
        clinic = obj.med_assistance.clinic
        if clinic:
            return mark_safe(
                f'<span style="font-weight: bold;" class="text-success">{clinic.name}, {clinic.city} ({clinic.county})</span>'
            )
        # return mark_safe('<i class="fas fa-times" style="font-weight: bold; color: red; font-size: 20px;"></i>')
        return

    assigned_clinic.short_description = _("Assigned Clinic")

    def requires_logistic_and_social_assistance(self, obj):
        transport = obj.logsol_assistance.transport_required
        transport_status_solved = obj.logsol_assistance.transport_status == "S"
        transport_icon_html = f'<i class="fas fa-car-side {"text-success" if transport_status_solved else "text-warning"}" style="font-weight: bold; font-size: 20px; margin-right: 10px;"></i>'

        accommodation = obj.logsol_assistance.accommodation_required
        accommodation_status_solved = obj.logsol_assistance.accommodation_status == "S"
        accommodation_icon_html = f'<i class="fas fa-house-user {"text-success" if accommodation_status_solved else "text-warning"}" style="font-weight: bold; font-size: 20px; margin-right: 10px;"></i>'

        assistance = obj.logsol_assistance.assistance_required
        assistance_status_solved = obj.logsol_assistance.assistance_status == "S"
        assistance_icon_html = f'<i class="fas fa-hands-helping {"text-success" if assistance_status_solved else "text-warning"}" style="font-weight: bold; font-size: 20px; margin-right: 10px;"></i>'

        if transport and not accommodation and not assistance:
            return mark_safe(transport_icon_html)
        if accommodation and not transport and not assistance:
            return mark_safe(accommodation_icon_html)
        if assistance and not transport and not accommodation:
            return mark_safe(assistance_icon_html)
        if transport and accommodation and not assistance:
            return mark_safe((transport_icon_html + accommodation_icon_html))
        if transport and assistance and not accommodation:
            return mark_safe((transport_icon_html + assistance_icon_html))
        if accommodation and assistance and not transport:
            return mark_safe((accommodation_icon_html + assistance_icon_html))
        if accommodation and assistance and transport:
            return mark_safe((transport_icon_html + accommodation_icon_html + assistance_icon_html))
        return None

    requires_logistic_and_social_assistance.short_description = _("Logistic & Social Assistance")

    def number_of_companions(self, obj):
        companions = obj.companions.count()
        if companions:
            return mark_safe(
                '<i class="fas fa-male text-success" style="font-weight: bold; font-size: 20px; margin-right: 10px;"></i>'
                * companions
            )

    number_of_companions.short_description = _("Companions")

    @admin.display(description=_("Case Status"))
    def case_status(self, obj):
        if obj.med_assistance and obj.med_assistance.clinic:
            badge_color, badge_text = "secondary", _("NO CASE STATUS")
            status = obj.med_assistance.case_status
            if status == "P":
                badge_color, badge_text = "warning", _("UNALLOCATED")
            if status == "R":
                badge_color, badge_text = "primary", _("ACCEPTED")
            if status == "T":
                badge_color, badge_text = "success", _("TAKEN")
            if status == "TP":
                badge_color, badge_text = "success", _("DIRECT CASE")
            return mark_safe(f'<span class="badge badge-{badge_color}">{badge_text}</span>')
        badge_color, badge_text = "secondary", _("NO CLINIC ASSIGNED")
        return mark_safe(f'<span class="badge badge-{badge_color}">{badge_text}</span>')

    list_display = [
        "get_full_name",
        "get_child_age",
        "sex",
        "tumor_type",
        "assigned_clinic",
        "case_status",
        "requires_logistic_and_social_assistance",
        "number_of_companions",
        "created_at",
    ]
    list_display_links = ["get_full_name"]
    search_fields = ["first_name", "last_name", "tumor_type"]
    readonly_fields = ("get_child_age",)
    list_filter = [
        "first_name",
        "last_name",
        "tumor_type",
        "med_assistance__case_status",
    ]

    ordering = ("pk",)

    view_on_site = False

    inlines = [
        MedicalAssistanceInLine,
        LogisticAndSocialAssistanceInLine,
        CompanionInLine,
        PatientRequestFileInLine,
    ]

    formfield_overrides = {
        TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 63})},
    }

    change_form_template = "admin/patient_request_admin.html"

    fieldsets = (
        (
            _("Identification"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "birth_date",
                    "get_child_age",
                    "sex",
                    "address",
                )
            },
        ),
        (
            _("Requester Data"),
            {
                "fields": (
                    "institution_type",
                    "institution_name",
                    "requester_first_name",
                    "requester_last_name",
                    "requester_phone_number",
                    "requester_email",
                ),
            },
        ),
        (
            _("Diagnostic"),
            {
                "fields": (
                    "diagnostic_class",
                    "known_complete_diagnostic",
                    "complete_diagnostic",
                    "date_diagnosed",
                    "diagnosing_institution_name",
                    "general_problem_description",
                    "medical_documents_checked",
                    "tumor_type",
                    "therapy_needs",
                    "other_therapy_needs",
                    "current_clinical_status",
                ),
            },
        ),
        (
            _("Child Location"),
            {
                "fields": (
                    "child_current_address",
                    "child_current_city",
                    "child_current_county",
                    "child_current_country",
                )
            },
        ),
        (
            _("Origin Medical Institution"),
            {
                "fields": (
                    "origin_medical_institution_name",
                    "origin_medical_institution_contact_person",
                    "origin_medical_institution_phone_number",
                    "origin_medical_institution_email",
                )
            },
        ),
    )

    jazzmin_section_order = (
        _("Identification"),
        _("Requester Data"),
        _("Diagnostic"),
        _("Origin Medical Institution"),
        _("Child Location"),
        _("Add Medical Assitance"),
        _("Logistical Info"),
        _("Add Logistic & Social Assistance"),
        _("Add Companion"),
        _("Upload Medical Files"),
    )
