from django.db import models
from django.contrib.auth.models import User 

class Booking(models.Model):
    SERVICE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE, related_name='bookings') 
    booking_date = models.DateTimeField() 
    status = models.CharField(max_length=10, choices=SERVICE_STATUS_CHOICES, default='pending') 

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.customer.username} - {self.service.name} on {self.booking_date.strftime('%Y-%m-%d %H:%M')}"

    def get_service_details(self):
        from services.models import Service 
        return self.service.description