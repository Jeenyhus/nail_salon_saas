from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField()  # E.g., 30 minutes
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    reserved = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    reservation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.client} - {self.service} on {self.appointment_date}"

class Payment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_reservation = models.BooleanField(default=False)
    is_final = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment of {self.amount} for {self.appointment}"

class Reminder(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    reminder_date = models.DateTimeField()

    def __str__(self):
        return f"Reminder for {self.appointment} on {self.reminder_date}"
