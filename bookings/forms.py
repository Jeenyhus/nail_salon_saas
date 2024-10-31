from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    """
    A form for creating new bookings

    Defines the fields that will be displayed in the form
    """
    class Meta:
        model = Booking
        fields = ['customer', 'service', 'booking_date', 'booking_time', 'notes']
