from django.contrib import admin

from .models import Appointment,Appointmentnote,Customer,Customernote,Location

for model in [Appointment,Appointmentnote,Customer,Customernote,Location]:
    admin.site.register(model)
