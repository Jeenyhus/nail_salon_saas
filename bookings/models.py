from django.db import models
from django.utils import timezone
from customers.models import Customer

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.CharField(max_length=100)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.customer} - {self.service}"
