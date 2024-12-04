from django import forms
from django.forms import ValidationError, inlineformset_factory
from django.urls import reverse_lazy

from touglates.widgets import TouglateDateInput, TouglatesRelatedSelect
from .models import Appointment, Appointmentnote, Customer, Customernote, Inquiry, Location
from django.contrib.admin.widgets import AdminDateWidget
from django.conf import settings
from django.apps import apps
from spl_members.models import Member as Staffmember

class CSVOptionForm(forms.Form):

    make_csv = forms.BooleanField(
        label="CSV",
        initial=False,
        required=False,
        help_text="Download the result as a CSV file",
    )


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "title",
            "customer",
            "request_summary",
            "customers_availability",
            "when_submitted",
            "staffer",
            "when_scheduled",
            "where_scheduled",
            "status",
        ]
        widgets = {
            "customer": TouglatesRelatedSelect(
                related_data={
                    "model_name": "Customer",
                    "app_name": "spl_discoveries",
                    "add_url": reverse_lazy("spl_discoveries:customer-popup"),
                },
            ),
            "staffer": TouglatesRelatedSelect(
                related_data={
                    "app_name": "spl_members",
                    "model_name": "Member",
                    "add_url": reverse_lazy("spl_discoveries:staffer-popup"),
                },
            ),
            "when_submitted": AdminDateWidget(),
            "when_scheduled": AdminDateWidget(),
        }


class AppointmentnoteForm(forms.ModelForm):
    class Meta:
        model = Appointmentnote
        fields = ["appointment", "when", "content"]


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name_full",
            "name_prefered",
            "email",
            "phone",
        ]


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            "name_full",
            "name_abbr",
        ]


def init_honeypot_fields(form, field_names):

    app_name = form.__module__.split('.')[0]
    form_name = form.__class__.__name__

    for field_name in field_names:
        try:
            form.fields[field_name].label=settings.HONEYPOT_FIELDS[app_name][form_name][field_name]["label"]
        except Exception as e:
            pass
        try:
            form.fields[field_name].help_text=settings.HONEYPOT_FIELDS[app_name][form_name][field_name]["help_text"]
        except Exception as e:
            pass

def honeypot_clean(field_names, cleaned_data):

    for field_name in field_names:
        field_value = cleaned_data.get(field_name)
        if field_value > "":
            raise ValidationError("There are fields which a person should realize are not to be completed", code='honeypot')


class InquiryForm(forms.ModelForm):

    honeypota = forms.CharField(max_length=100, required=False  )
    honeypotb = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        init_honeypot_fields(self, self.declared_fields)

    def clean(self):
        cleaned_data = super().clean()
        honeypot_clean(self.declared_fields, cleaned_data)

    class Meta:
        model = Inquiry
        fields=[
            "name_full",
            "name_prefered",
            "availability",
            "summary",
            "details",
            "where_desired",
        ]


class CustomernoteForm(forms.ModelForm):
    class Meta:
        model = Customernote
        fields = ["customer", "when", "content"]


class StaffmemberForm(forms.ModelForm):
    class Meta:
        model = Staffmember
        fields = [
            "name_full",
            "email",
            "phone",
        ]


AppointmentAppointmentnoteFormset = inlineformset_factory(
    Appointment, Appointmentnote, form=AppointmentnoteForm, extra=10
)
CustomerCustomernoteFormset = inlineformset_factory(
    Customer, Customernote, form=CustomernoteForm, extra=10
)
