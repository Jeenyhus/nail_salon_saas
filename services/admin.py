from django.contrib import admin
from .models import Service, Appointment, Payment, ClientProfile, Notification

# Register your models here.
admin.site.register(Service)
admin.site.register(Appointment)
admin.site.register(Payment)
admin.site.register(ClientProfile)
admin.site.register(Notification)