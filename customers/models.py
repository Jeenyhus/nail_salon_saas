"""
This module contains the customer app models for the nail salon application. It includes the following models:
- Customer: Represents a customer with personal details.
- CustomerInteraction: Represents interactions between the salon and customers.
- CustomerLoyalty: Represents the loyalty points system for customers.
"""

from django.db import models

class Customer(models.Model):
    """
    Model representing a customer.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CustomerInteraction(models.Model):
    """
    Model representing an interaction between the salon and a customer.
    """
    INTERACTION_CHOICES = [
        ('appointment', 'Appointment'),
        ('complaint', 'Complaint'),
        ('inquiry', 'Inquiry'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.interaction_type} with {self.customer} on {self.date}"


class CustomerLoyalty(models.Model):
    """
    Model representing the loyalty points system for a customer.
    """
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer} - {self.points} points"
