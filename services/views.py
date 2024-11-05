from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Service, Appointment, Payment, Reminder
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # You could also save this to a database if desired
        # For now, we send an email
        
        full_message = f"Message from {name} ({email}):\n\n{message}"
        
        send_mail(
            subject="New Contact Inquiry",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL]
        )
        
        return redirect('home')  # Redirect to the home page after submission

    return render(request, 'contact.html')


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

signup_view = SignUpView.as_view()


def about_view(request):
    return render(request, 'about.html')

def home_view(request):
    popular_services = Service.objects.all()[:3]
    return render(request, 'home.html', {'popular_services': popular_services})


@login_required
def catalog_view(request):
    services = Service.objects.all()
    return render(request, 'services/catalog.html', {'services': services})

@login_required
def book_appointment(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == "POST":
        appointment_date = request.POST.get('appointment_date')
        reservation_fee = service.price * 0.10  # 10% reservation fee

        appointment = Appointment.objects.create(
            client=request.user,
            service=service,
            appointment_date=appointment_date,
            reserved=True,
            reservation_fee=reservation_fee
        )

        # Process payment for the reservation fee here
        # e.g., initiate_payment(appointment, amount=reservation_fee, is_reservation=True)

        # Schedule reminders
        Reminder.objects.create(
            appointment=appointment,
            reminder_date=appointment_date - timedelta(hours=48)
        )
        Reminder.objects.create(
            appointment=appointment,
            reminder_date=appointment_date - timedelta(hours=4)
        )

        return redirect('confirm_booking', appointment_id=appointment.id)
    return render(request, 'services/book_appointment.html', {'service': service})

@login_required
def confirm_booking(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'services/confirm_booking.html', {'appointment': appointment})

@login_required
def complete_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == "POST":
        # Final payment processing
        Payment.objects.create(
            appointment=appointment,
            amount=appointment.service.price - appointment.reservation_fee,
            is_final=True
        )
        appointment.completed = True
        appointment.save()
        return redirect('thank_you')

    return render(request, 'services/complete_payment.html', {'appointment': appointment})
