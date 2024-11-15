import csv
import logging
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.db.models import Q
from django.forms import BaseModelForm
from django.http import QueryDict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView

from django_filters_stoex.forms import FilterstoreRetrieveForm, FilterstoreSaveForm
from django_filters_stoex.views import FilterView
from spl_members.models import Member as Staffmember
from touglates.views import make_labels

from .filterset import AppointmentFilter, CustomerFilter
from .forms import (
    AppointmentAppointmentnoteFormset,
    AppointmentForm,
    CustomerCustomernoteFormset,
    CustomerForm,
    LocationForm,
    StaffmemberForm,
)
from .models import Appointment, Appointmentnote, Customer, Location

logger = logging.getLogger(__name__)


class AppointmentCreate(PermissionRequiredMixin, CreateView):
    permission_required = "spl_discoveries.add_appointment"
    model = Appointment
    form_class = AppointmentForm
    template_name = "spl_discoveries/appointment_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "appointmentnotes": AppointmentAppointmentnoteFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(self.request.POST)
            else:
                context_data[formsetkey] = formsetclass()

        appointment_labels = make_labels(Appointment)

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "appointmentnotes": AppointmentAppointmentnoteFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy(
            "spl_discoveries:appointment-detail", kwargs={"pk": self.object.pk}
        )

    def form_invalid(self, form):

        return super().form_invalid(form)

class AppointmentUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "spl_discoveries.change_appointment"
    model = Appointment
    form_class = AppointmentForm
    template_name = "spl_discoveries/appointment_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "appointmentnotes": AppointmentAppointmentnoteFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                context_data[formsetkey] = formsetclass(instance=self.object)

        appointment_labels = make_labels(Appointment)

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save()

        formsetclasses = {
            "notes": AppointmentAppointmentnoteFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        if "popup" in self.kwargs:
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy(
            "spl_discoveries:appointment-detail", kwargs={"pk": self.object.pk}
        )


class AppointmentDetail(PermissionRequiredMixin, DetailView):
    permission_required = "spl_discoveries.view_appointment"
    model = Appointment

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["appointment_labels"] = make_labels(Appointment)

        context_data["appointmentnote_labels"] = make_labels(Appointmentnote)

        return context_data


class AppointmentDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "spl_discoveries.delete_appointment"
    model = Appointment
    success_url = reverse_lazy("spl_discoveries:appointment-list")

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)
        context_data["appointment_labels"] = make_labels(Appointment)
        print("tp23be625", context_data["appointment_labels"])
        context_data["appointmentnote_labels"] = make_labels(Appointmentnote)
        return context_data

class AppointmentList(PermissionRequiredMixin, FilterView):
    permission_required = "spl_discoveries.view_appointment"
    filterset_class = AppointmentFilter
    filterstore_urlname = "spl_discoveries:appointment-filterstore"
    model=Appointment

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm()
        context_data["filterstore_save"] = FilterstoreSaveForm()
        context_data["count"] = self.object_list.count()
        context_data["appoitment_labels"] = make_labels(Appointment)
        return context_data


class AppointmentClose(PermissionRequiredMixin, DetailView):
    permission_required = "spl_discoveries.view_appointment"
    model = Appointment
    template_name = "spl_discoveries/appointment_closer.html"


class CustomerCreate(PermissionRequiredMixin, CreateView):
    permission_required = "spl_discoveries.add_customer"
    model = Customer
    form_class = CustomerForm
    template_name = "spl_discoveries/customer_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "customernotes": CustomerCustomernoteFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(self.request.POST)
            else:
                context_data[formsetkey] = formsetclass()

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "notes": CustomerCustomernoteFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy(
            "spl_discoveries:customer-detail", kwargs={"pk": self.object.pk}
        )


class CustomerUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "spl_discoveries.change_customer"
    model = Customer
    form_class = CustomerForm
    template_name = "spl_discoveries/customer_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "notes": CustomerCustomernoteFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                context_data[formsetkey] = formsetclass(instance=self.object)

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save()

        formsetclasses = {
            "notes": CustomerCustomernoteFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        if "popup" in self.kwargs:
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy(
            "spl_discoveries:customer-detail", kwargs={"pk": self.object.pk}
        )


class CustomerDetail(PermissionRequiredMixin, DetailView):
    permission_required = "spl_discoveries.view_customer"
    model = Customer

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["customer_labels"] = make_labels(Customer)

        return context_data


class CustomerDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "spl_discoveries.delete_customer"
    model = Customer
    success_url = reverse_lazy("spl_discoveries:customer-list")


class CustomerList(PermissionRequiredMixin, FilterView):
    permission_required = "spl_discoveries.view_customer"
    filterset_class = CustomerFilter
    filterstore_urlname = "spl_discoveries:customer-filterstore"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm()
        context_data["filterstore_save"] = FilterstoreSaveForm()
        context_data["count"] = self.object_list.count()
        context_data["labels"] = make_labels(Customer)
        return context_data


class LocationCreate(PermissionRequiredMixin, CreateView):
    permission_required = "discovery_locations.add_location"
    model = Location
    form_class = LocationForm
    template_name = "discovery_locations/location_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "notes": LocationLocationnoteFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(self.request.POST)
            else:
                context_data[formsetkey] = formsetclass()

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "notes": LocationLocationnoteFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy(
            "discovery_locations:location-detail", kwargs={"pk": self.object.pk}
        )


class LocationUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "discovery_locations.change_location"
    model = Location
    form_class = LocationForm
    template_name = "discovery_locations/location_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "notes": LocationLocationnoteFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                context_data[formsetkey] = formsetclass(instance=self.object)

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save()

        formsetclasses = {
            "notes": LocationLocationnoteFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        if "popup" in self.kwargs:
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy(
            "discovery_locations:location-detail", kwargs={"pk": self.object.pk}
        )


class LocationDetail(PermissionRequiredMixin, DetailView):
    permission_required = "discovery_locations.view_location"
    model = Location

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["location_labels"] = make_labels(Location)

        return context_data


class LocationDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "discovery_locations.delete_location"
    model = Location
    success_url = reverse_lazy("discovery_locations:location-list")


class LocationList(PermissionRequiredMixin, ListView):
    permission_required = "discovery_locations.view_location"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm()
        context_data["filterstore_save"] = FilterstoreSaveForm()
        context_data["count"] = self.object_list.count()
        context_data["labels"] = make_labels(Location)
        return context_data


class StaffmemberCreate(PermissionRequiredMixin, CreateView):
    permission_required = "spl_members.add_member"
    model = Staffmember
    form_class = StaffmemberForm
    template_name = "spl_discoveries/staffmember_create.html"

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "spl_members",
                    "model_name": "Member",
                },
            )
        return reverse_lazy(
            "spl_discoveries:staffmember-detail", kwargs={"pk": self.object.pk}
        )


class StaffmemberDetail(PermissionRequiredMixin, DetailView):
    permission_required = "spl_discoveries.view_staffmember"
    model = Staffmember

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["staffmember_labels"] = make_labels(Staffmember)

        return context_data
