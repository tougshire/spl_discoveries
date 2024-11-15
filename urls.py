from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from . import views
from django.views.i18n import JavaScriptCatalog

app_name = "spl_discoveries"

urlpatterns = [
    path(
        "",
        RedirectView.as_view(url=reverse_lazy("spl_discoveries:appointment-list")),
    ),
    path(
        "appointment/",
        RedirectView.as_view(url=reverse_lazy("spl_discoveries:appointment-list")),
    ),
    path(
        "appointment/create/",
        views.AppointmentCreate.as_view(),
        name="appointment-create",
    ),
    path(
        "appointment/<int:pk>/update/",
        views.AppointmentUpdate.as_view(),
        name="appointment-update",
    ),
    path(
        "appointment/<int:pk>/detail/",
        views.AppointmentDetail.as_view(),
        name="appointment-detail",
    ),
    path(
        "appointment/<int:pk>/delete/",
        views.AppointmentDelete.as_view(),
        name="appointment-delete",
    ),
    path(
        "appointment/list/filterstore/<int:from_store>/",
        views.AppointmentList.as_view(),
        name="appointment-filterstore",
    ),
    path(
        "appointment/list/",
        views.AppointmentList.as_view(),
        name="appointment-list",
    ),
    path(
        "appointment/<str:copied_from>/copied/",
        views.AppointmentList.as_view(),
        name="appointment-copied",
    ),
    path(
        "customer/",
        RedirectView.as_view(url=reverse_lazy("spl_discoveries:customer-list")),
    ),
    path("customer/create/", views.CustomerCreate.as_view(), name="customer-create"),
    path("customer/popup/", views.CustomerCreate.as_view(), name="customer-popup"),
    path(
        "customer/<int:pk>/update/",
        views.CustomerUpdate.as_view(),
        name="customer-update",
    ),
    path(
        "customer/<int:pk>/detail/",
        views.CustomerDetail.as_view(),
        name="customer-detail",
    ),
    path(
        "customer/<int:pk>/delete/",
        views.CustomerDelete.as_view(),
        name="customer-delete",
    ),
    path("customer/list/", views.CustomerList.as_view(), name="customer-list"),
    path(
        "staffer/",
        RedirectView.as_view(url=reverse_lazy("spl_discoveries:staffer-list")),
    ),
    path("staffer/popup/", views.StaffmemberCreate.as_view(), name="staffer-popup"),
    path(
        "staffer/<int:pk>/detail/",
        views.StaffmemberDetail.as_view(),
        name="staffer-detail",
    ),
    path(
        "location/",
        RedirectView.as_view(url=reverse_lazy("spl_discoveries:location-list")),
    ),
    path("location/create/", views.LocationCreate.as_view(), name="location-create"),
    path("location/popup/", views.LocationCreate.as_view(), name="location-popup"),
    path(
        "location/<int:pk>/update/",
        views.LocationUpdate.as_view(),
        name="location-update",
    ),
    path(
        "location/<int:pk>/detail/",
        views.LocationDetail.as_view(),
        name="location-detail",
    ),
    path(
        "location/<int:pk>/delete/",
        views.LocationDelete.as_view(),
        name="location-delete",
    ),
    path("location/list/", views.LocationList.as_view(), name="location-list"),
    path(
        "appointmentnote/",
        RedirectView.as_view(url=reverse_lazy("spl_discoveries:appointmentnote-list")),
    ),
    path(
        "jsi18n",
        JavaScriptCatalog.as_view(),
        name="js-catlog",
    ),
]
