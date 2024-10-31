from django.contrib import admin
from .models import Customer, CustomerInteraction, CustomerLoyalty

# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerInteraction)
admin.site.register(CustomerLoyalty)