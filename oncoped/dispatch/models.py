from email.policy import default
from tabnanny import verbose

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

SEX_CHOICES = (
    ("M", _("Male")),
    ("F", _("Female")),
    ("O", _("Other / Unspecified")),
)

TUMOR_TYPE_CHOICES = (("S", _("Solid")), ("H", _("Hematologic")))

THERAPY_NEEDS_CHOICES = (
    ("CHE", _("Chemotherapy")),
    ("SUR", _("Surgical")),
    ("PAL", _("Palliative")),
    ("MON", _("Monitoring")),
    ("INV", _("Diagnostic Investigation")),
    ("SUT", _("Supportive Treatment")),
    ("RAD", _("Radiotherapy")),
    ("TRA", _("Transplant")),
    ("OTH", _("Other")),
)

REQUESTER_TYPE = (
    ("MED", _("Medical Institution")),
    ("NGO", _("Non-Governmental Organization")),
    ("PER", _("Person")),
    ("COM", _("Company")),
)

TRANSPORT_CHOICES = (
    ("NAT", _("National")),
    ("INT", _("International")),
)

DIAGNOSTIC_CLASS_CHOICES = (
    (
        "LAMM",
        "Leucemii, afecțiuni mieloproliferative și mielodisplazice",
    ),
    (
        "LNR",
        "Limfoame și neoplasme reticuloendoteliale",
    ),
    (
        "SNCNII",
        "SNC și neoplasme intracraniene și intraspinale",
    ),
    (
        "NATCNP",
        "Neuroblastom și alte tumori ale celulelor nervoase periferice",
    ),
    (
        "R",
        "Retinoblastom",
    ),
    (
        "TR",
        "Tumori renale",
    ),
    (
        "TH",
        "Tumori hepatice",
    ),
    (
        "TMO",
        "Tumori maligne ale oaselor",
    ),
    (
        "SPMATE",
        "Sarcoame de părți moi și alte țesuturi extraosoase",
    ),
    (
        "TTNG",
        "Tumori terofoblastice și neoplasme ale gonadelor",
    ),
    (
        "ANMEMM",
        "Alte neoplasme maligne epiteliale și melanoame maligne",
    ),
    (
        "ANMN",
        "Alte neoplasme maligne nespecificate",
    ),
)

CASE_STATUS_CHOICES = (
    ("P", _("Case Pending")),
    ("R", _("Clinic is Ready for takeover")),
    ("T", _("Taken over by Clinic")),
    ("TP", _("Taken over previously, in person")),
    ("RE", _("Redirected")),
)

LOGISTIC_STATUS_CHOICES = (
    ("US", _("Unsolved")),
    ("S", _("Solved")),
)

YES_NO_CHOICES = (
    (1, _("Yes")),
    (0, _("No")),
)

class Clinic(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    tumor_type = MultiSelectField(
        verbose_name=_("Tumor Type"),
        max_length=3,
        choices=TUMOR_TYPE_CHOICES,
        blank=False,
    )
    therapy_services = MultiSelectField(
        verbose_name=_("Therapy Services"),
        choices=THERAPY_NEEDS_CHOICES,
        blank=False,
    )
    name = models.CharField(
        verbose_name=_("Clinic Name"),
        max_length=150,
        blank=False,
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=100,
        blank=False,
    )
    county = models.CharField(
        verbose_name=_("County"),
        max_length=3,
        choices=settings.COUNTY_CHOICES,
        blank=False,
    )
    address = models.CharField(
        verbose_name=_("Address"),
        max_length=250,
        blank=False,
    )
    hospitalization_office_email = models.EmailField(verbose_name=_("Hospitalization Office Email"), blank=False)
    hospitalization_office_phone_number = models.CharField(
        verbose_name=_("Hospitalization Office Phone Number"),
        max_length=30,
        blank=False,
    )
    head_of_dept_name = models.CharField(
        verbose_name=_("Head Of Department Name"),
        max_length=100,
        blank=False,
    )
    head_of_dept_email = models.EmailField(verbose_name=_("Head Of Department Email"), blank=False)
    dept_phone = models.CharField(
        verbose_name=_("Department Phone Number"),
        max_length=30,
        blank=False,
    )
    available_beds = models.SmallIntegerField(verbose_name=_("Available Beds"), blank=False, default=0)

    def __str__(self):
        return f"{self.name}, {self.city} ({self.county}) - {self.available_beds} {_('Beds')}"

    class Meta:
        verbose_name = _("Clinic")
        verbose_name_plural = _("Clinics")


class PatientRequest(models.Model):
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)

    # Identification

    first_name = models.CharField(verbose_name=_("First Name"), max_length=100, blank=False)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=100, blank=False)
    birth_date = models.DateField(verbose_name=_("Birth Date"), blank=False)
    sex = models.CharField(verbose_name=_("Sex"), max_length=2, choices=SEX_CHOICES, default="PAS", blank=False)
    address = models.CharField(verbose_name=_("Address"), max_length=250, blank=False)

    # Requester
    institution_type = models.CharField(
        verbose_name=_("Requester Type"),
        max_length=3,
        choices=REQUESTER_TYPE,
        default="MED",
        blank=False,
    )
    institution_name = models.CharField(
        verbose_name=_("Organization Name"),
        max_length=250,
        blank=True,
        help_text=_("Fill in only if requester is not a Person"),
    )
    requester_first_name = models.CharField(
        verbose_name=_("Requester First Name"),
        max_length=100,
        blank=False,
    )
    requester_last_name = models.CharField(
        verbose_name=_("Requester Last Name"),
        max_length=100,
        blank=False,
    )
    requester_phone_number = models.CharField(
        verbose_name=_("Requester Phone Number"),
        max_length=30,
        help_text=_("Please include country prefix e.g. +40723000123"),
        blank=False,
    )
    requester_email = models.EmailField(
        verbose_name=_("Requester Email"),
        blank=False,
    )

    # Diagnostic
    diagnostic_class = models.CharField(
        verbose_name=_("Diagnostic Class"), max_length=10, choices=DIAGNOSTIC_CLASS_CHOICES, blank=True
    )
    known_complete_diagnostic = models.CharField(verbose_name=_("Complete Diagnostic Known"), choices=YES_NO_CHOICES, default=0, max_length=2)
    complete_diagnostic = models.TextField(verbose_name=_("Complete Diagnostic"), blank=True)
    date_diagnosed = models.DateField(verbose_name=_("Date Diagnosed"), blank=True, null=True)
    diagnosing_institution_name = models.CharField(
        verbose_name=_("Diagnosing Institution Name"), max_length=150, blank=True
    )
    general_problem_description = models.TextField(
        verbose_name=_("General Problem Description"),
        help_text="Describe the Child's medical issue",
        blank=True,
    )
    medical_documents_checked = models.BooleanField(verbose_name=_("Medical Documents Checked"), default=False)
    tumor_type = models.CharField(verbose_name=_("Tumor Type"), max_length=2, choices=TUMOR_TYPE_CHOICES, blank=True)
    therapy_needs = MultiSelectField(verbose_name=_("Therapy Needs"), choices=THERAPY_NEEDS_CHOICES, blank=True)
    other_therapy_needs = models.CharField(verbose_name=_("Other Therapy Needs"), max_length=250, blank=True)
    current_clinical_status = models.TextField(verbose_name=_("Current Clinical Status"), blank=True)

    # Location details
    child_current_address = models.CharField(verbose_name=_("Child Current Address"), max_length=100, blank=True)
    child_current_city = models.CharField(verbose_name=_("Child Current City"), max_length=100, blank=True)
    child_current_county = models.CharField(verbose_name=_("Child Current County"), max_length=100, blank=True)
    child_current_country = models.CharField(verbose_name=_("Child Current Country"), max_length=100, blank=True)

    # Origin Institution
    origin_medical_institution_name = models.CharField(verbose_name=_("Institution Name"), max_length=150, blank=True)
    origin_medical_institution_contact_person = models.CharField(
        verbose_name=_("Contact Person"), max_length=150, blank=True, help_text=_("Full Name of the contact person")
    )
    origin_medical_institution_phone_number = models.CharField(
        verbose_name=_("Phone Number"),
        max_length=30,
        help_text=_("Contact Person's phone number. Please include country prefix e.g. +40723000123"),
        blank=True,
    )
    origin_medical_institution_email = models.EmailField(verbose_name=_("Email"), blank=True)

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    get_full_name.short_description = _("Full Name")

    def get_child_age(self):
        today = timezone.localdate()
        age = relativedelta(self.birth_date, today)

        return -age.years

    get_child_age.short_description = _("Age")

    def __str__(self):
        return f"#{self.id} {self.get_full_name()} {self.get_child_age()}{self.sex}"

    def validate_unique(self, exclude=None):
        try:
            super().validate_unique()
        except ValidationError as e:
            raise ValidationError(_("There is already a Pacient Request with this name, birth date and age."))

    class Meta:
        verbose_name = _("Patient Request")
        verbose_name_plural = _("Patient Requests")
        unique_together = ["first_name", "last_name", "birth_date"]


def patient_request_upload(instance, filename):
    file_name = filename.lower().replace(" ", "_")
    return f"patient_request_files/{filename}"


class PatientRequestFile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    request = models.ForeignKey(PatientRequest, on_delete=models.CASCADE)
    file = models.FileField(upload_to=patient_request_upload, null=True, blank=True)


class MedicalAssistance(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    request = models.OneToOneField(PatientRequest, on_delete=models.CASCADE, related_name="med_assistance")

    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True, related_name="rel_clinics")

    case_status = models.CharField(
        verbose_name=_("Case Status"), choices=CASE_STATUS_CHOICES, max_length=3, default="P", blank=False
    )
    estimated_arrival_date = models.DateField(verbose_name=_("Estimated Arrival Date"), null=True, blank=True)
    hospitalization_start = models.DateField(
        verbose_name=_("Hospitalization Start"),
        null=True,
        blank=True,
        help_text=_("Only with confirmation from the receiving clinic!"),
    )
    receiving_dr_full_name = models.CharField(verbose_name=_("Receiving Dr Full Name"), max_length=150, blank=True)
    comments = models.TextField(verbose_name=_("Comments"), blank=True)
    international_redirect = models.BooleanField(verbose_name=_("International Redirect"), default=False)
    redirect_institution = models.CharField(verbose_name=_("Redirect Institution"), max_length=250, blank=True)
    specialty = models.CharField(verbose_name=_("Specialty"), max_length=150, blank=True)
    location = models.TextField(verbose_name=_("Location"), max_length=250, blank=True, help_text=_("Location: City, Country"))
    reason = models.TextField(verbose_name=_("Reason"), blank=True)

    def __str__(self):
        pre = _("Medical Assistance")
        return f"{pre} {self.id}"


class LogisticAndSocialAssistance(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    request = models.OneToOneField(PatientRequest, on_delete=models.CASCADE, related_name="logsol_assistance")

    # Transport
    transport_required = models.BooleanField(
        verbose_name=_("Transport Required"),
        default=False,
        help_text=_("Wether national or international transportation is required for this assistence"),
    )
    transport_status = models.CharField(
        verbose_name=_("Transport Status"),
        max_length=2,
        choices=LOGISTIC_STATUS_CHOICES,
        default="US",
        blank=False,
    )
    transport = models.CharField(
        verbose_name=_("Transport"), max_length=3, choices=TRANSPORT_CHOICES, blank=True, default="NAT"
    )
    pick_up_location = models.CharField(
        verbose_name=_("Pick Up Location"),
        max_length=200,
        blank=True,
        help_text=_("Departing from: City, Country"),
    )
    destination_location = models.CharField(
        verbose_name=_("Pick Up Location"),
        max_length=200,
        blank=True,
        help_text=_("Departing from: City, Country"),
    )
    transport_details = models.TextField(verbose_name=_("Transport Details"), blank=True)
    transport_rep_external = models.BooleanField(
        verbose_name=_("External Transport Representative"),
        default=False,
        help_text=_("Is the transport representative external to the organization?"),
    )
    transport_rep_external_details = models.TextField(
        verbose_name=_("External Transport Representantive Details"), blank=True
    )

    # Accommodation
    accommodation_required = models.BooleanField(
        verbose_name=_("Accommodation Required"),
        default=False,
        help_text=_("Wether accommodation is required for this assistence"),
    )
    accommodation_status = models.CharField(
        verbose_name=_("Accommodation Status"),
        max_length=2,
        choices=LOGISTIC_STATUS_CHOICES,
        default="US",
        blank=False,
    )
    accommodation_details = models.TextField(verbose_name=_("Accommodation Details"), null=True, blank=True)
    accommodation_rep_external = models.BooleanField(
        verbose_name=_("External accommodation Representative"),
        default=False,
        help_text=_("Is the accommodation representative external to the organization?"),
    )
    accommodation_rep_external_details = models.TextField(
        verbose_name=_("External Accommodation Representantive Details"), blank=True
    )

    # Assistance
    assistance_required = models.BooleanField(
        verbose_name=_("Assistance Required"), default=False, help_text=_("Wether assistance is required")
    )
    assistance_status = models.CharField(
        verbose_name=_("Assistance Status"),
        max_length=2,
        choices=LOGISTIC_STATUS_CHOICES,
        default="US",
        blank=False,
    )
    assistance_rep_external = models.BooleanField(
        verbose_name=_("External Assistance Representative"),
        default=False,
        help_text=_("Is the assistance representative external to the organization?"),
    )
    assistance_rep_external_details = models.TextField(
        verbose_name=_("External Assistance Representantive Details"), blank=True
    )

    def __str__(self):
        name = _("Logistic & Transport")
        return f"{name} {self.id}"


class Companion(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    request = models.ForeignKey(PatientRequest, on_delete=models.CASCADE, related_name="companions")

    companion_name = models.CharField(verbose_name=_("Companion Name"), max_length=150, blank=True)
    companion_relationship = models.CharField(verbose_name=_("Companion Relationship"), max_length=150, blank=True)
    companion_phone_number = models.CharField(
        verbose_name=_("Companion Phone Number"),
        max_length=30,
        help_text=_("Please include country prefix e.g. +40723000123"),
        blank=True,
    )
    companion_other_details = models.TextField(verbose_name=_("Companion Other Details"), blank=True)

    def __str__(self):
        name = _("Companion")
        return f"{name} {self.id}"
