from django import forms
from django.forms import inlineformset_factory
from django.urls import reverse_lazy

from spl_members.models import Member as Staffmember
from touglates.widgets import TouglatesRelatedSelect
from .models import Appointment, Appointmentnote, Customer, Customernote, Location
from django.contrib.admin.widgets import AdminDateWidget


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
