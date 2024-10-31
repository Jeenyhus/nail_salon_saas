from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Booking

class BookingListView(ListView):
    """
    Displays a list of all bookings.
    """
    model = Booking
    template_name = "bookings/booking_list.html"
    context_object_name = "bookings"


class BookingDetailView(DetailView):
    """
    Displays the details of a single booking.
    """
    model = Booking
    template_name = "bookings/booking_detail.html"
    context_object_name = "booking"


class BookingCreateView(CreateView):
    """
    Allows the creation of a new booking.
    """
    model = Booking
    fields = ['customer', 'service', 'booking_date', 'booking_time', 'notes']
    template_name = "bookings/booking_form.html"
    success_url = reverse_lazy('booking_list')


class BookingUpdateView(UpdateView):
    """
    Allows updating an existing booking.
    """
    model = Booking
    fields = ['customer', 'service', 'booking_date', 'booking_time', 'status', 'notes']
    template_name = "bookings/booking_form.html"
    success_url = reverse_lazy('booking_list')
