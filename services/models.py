from django.db import models
from .models import Service
"""
This module defines the Service model for the nail salon application.

Classes:
    Service: A Django model representing a service offered by the nail salon.
"""

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.name