from django.db import models
from django.contrib.auth.models import User

class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name="Service Title", help_text="Enter the title of the service")
    description = models.TextField(verbose_name="Service Description", help_text="Enter a detailed description of the service")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Service Price", help_text="Enter the price of the service")
    image = models.ImageField(upload_to='service_images/', blank=True, null=True, verbose_name="Service Image", help_text="Upload an image for the service")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['title']

class Appointment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Client", help_text="Select the client for the appointment")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Service", help_text="Select the service for the appointment")
    appointment_date = models.DateTimeField(verbose_name="Appointment Date", help_text="Enter the date and time of the appointment")
    reserved = models.BooleanField(default=False, verbose_name="Reserved", help_text="Indicates if the appointment is reserved")
    completed = models.BooleanField(default=False, verbose_name="Completed", help_text="Indicates if the appointment is completed")
    reservation_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Reservation Fee", help_text="Enter the reservation fee for the appointment")

    def __str__(self):
        return f"{self.client.username} - {self.service.title} on {self.appointment_date}"

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
        ordering = ['appointment_date']

class Payment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name="Appointment", help_text="Select the appointment for the payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Payment Amount", help_text="Enter the amount of the payment")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Payment Timestamp", help_text="The time when the payment was made")
    is_reservation = models.BooleanField(default=False, verbose_name="Is Reservation", help_text="Indicates if the payment is for a reservation")
    is_final = models.BooleanField(default=False, verbose_name="Is Final", help_text="Indicates if the payment is the final payment")

    def __str__(self):
        return f"Payment of {self.amount} for {self.appointment}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-timestamp']

class Reminder(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, verbose_name="Appointment", help_text="Select the appointment for the reminder")
    reminder_date = models.DateTimeField(verbose_name="Reminder Date", help_text="Enter the date and time for the reminder")

    def __str__(self):
        return f"Reminder for {self.appointment} on {self.reminder_date}"

    class Meta:
        verbose_name = "Reminder"
        verbose_name_plural = "Reminders"
        ordering = ['reminder_date']
