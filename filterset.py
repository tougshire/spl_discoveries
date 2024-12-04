from django.http import QueryDict
import django_filters

from django_filters_stoex.filterset import StoexFilterSet
from spl_members.models import Member as Staffmember
from .models import Appointment, Customer, Inquiry
from django.db import models
from django import forms
from django_filters_stoex.filters import CrossFieldSearchFilter
from touglates.widgets import DropdownSelectMultiple


class AppointmentFilter(StoexFilterSet):

    combined_text_search = CrossFieldSearchFilter(
        label="Text Search",
        field_name="customer__name_full,staffer__name_full,staffer__name_prefered,where_scheduled__name_full,where_scheduled__name_abbr",
        lookup_expr="icontains",
    )
    customer = django_filters.ModelMultipleChoiceFilter(
        widget=DropdownSelectMultiple,
        field_name="customer",
        label="Customer",
        queryset=Customer.objects.all(),
    )
    staffer = django_filters.ModelMultipleChoiceFilter(
        widget=DropdownSelectMultiple,
        field_name="staffer",
        label="Staffer",
        queryset=Staffmember.objects.all(),
    )

    status__in = django_filters.MultipleChoiceFilter(
        widget=DropdownSelectMultiple,
        field_name="status",
        label="Status",
        choices=Appointment._meta.get_field("status").choices,
    )

    orderbyfields = django_filters.OrderingFilter(
        fields=(
            "when_submitted",
            "status",
            "customer",
            "staffer",
        ),
    )

    class Meta:
        model = Appointment
        fields = []


class CustomerFilter(StoexFilterSet):

    name_search = CrossFieldSearchFilter(
        label="Text Search",
        field_name="name_full, name_prefered, email, phone",
        lookup_expr="icontains",
    )
    customer = django_filters.ModelMultipleChoiceFilter(
        widget=DropdownSelectMultiple,
        field_name="customer",
        label="Customer",
        queryset=Customer.objects.all(),
    )
    staffer = django_filters.ModelMultipleChoiceFilter(
        widget=DropdownSelectMultiple,
        field_name="staffer",
        label="Staffer",
        queryset=Staffmember.objects.all(),
    )

    status__in = django_filters.MultipleChoiceFilter(
        widget=DropdownSelectMultiple,
        field_name="status",
        label="Status",
        choices=Appointment._meta.get_field("status").choices,
    )

    orderbyfields = django_filters.OrderingFilter(
        fields=(
            "name_full",
            "name_prefered",
            "email",
        ),
    )

    class Meta:
        model = Appointment
        fields = []

class InquiryFilter(StoexFilterSet):

    combined_text_search = CrossFieldSearchFilter(
        label="Text Search",
        field_name="name_full,name_prefered,where_desired__name_full,where_desired__name_abbr",
        lookup_expr="icontains",
    )

    orderbyfields = django_filters.OrderingFilter(
        fields=(
            "when_submitted",
            "name_full",
        ),
    )

    class Meta:
        model = Inquiry
        fields = []
