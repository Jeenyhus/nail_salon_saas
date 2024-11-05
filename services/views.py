import logging
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
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django import forms
from django.contrib import messages

logger = logging.getLogger(__name__)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            full_message = f"Message from {name} ({email}):\n\n{message}"
            
            try:
                send_mail(
                    subject="New Contact Inquiry",
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL]
                )
                messages.success(request, 'Your message has been sent successfully.')
            except Exception as e:
                logger.error(f"Error sending contact email: {e}")
                messages.error(request, 'There was an error sending your message. Please try again later.')
            
            return redirect('home')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

signup_view = SignUpView.as_view()

def about_view(request):
    return render(request, 'about.html')

class CustomLoginView(LoginView):
    def form_valid(self, form):
        login(self.request, form.get_user())
        
        if self.request.user.is_staff:
            return redirect('dashboard')
        else:
            return redirect('home')

def home_view(request):
    popular_services = Service.objects.all()[:3]
    return render(request, 'home.html', {'popular_services': popular_services})

@login_required
def dashboard(request):
    services = Service.objects.all()
    appointments = Appointment.objects.select_related('client', 'service').all()
    payments = Payment.objects.select_related('appointment').all()
    reminders = Reminder.objects.select_related('appointment').all()

    context = {
        'services': services,
        'appointments': appointments,
        'payments': payments,
        'reminders': reminders,
    }
    return render(request, 'services/dashboard.html', context)

@login_required
def catalog_view(request):
    services = Service.objects.all()
    return render(request, 'services/catalog.html', {'services': services})

@login_required
def book_appointment(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == "POST":
        appointment_date = request.POST.get('appointment_date')
        reservation_fee = service.price * 0.10

        try:
            appointment = Appointment.objects.create(
                client=request.user,
                service=service,
                appointment_date=appointment_date,
                reserved=True,
                reservation_fee=reservation_fee
            )

            Reminder.objects.create(
                appointment=appointment,
                reminder_date=appointment_date - timedelta(hours=48)
            )
            Reminder.objects.create(
                appointment=appointment,
                reminder_date=appointment_date - timedelta(hours=4)
            )

            messages.success(request, 'Your appointment has been booked successfully.')
            return redirect('confirm_booking', appointment_id=appointment.id)
        except Exception as e:
            logger.error(f"Error booking appointment: {e}")
            messages.error(request, 'There was an error booking your appointment. Please try again later.')

    return render(request, 'services/book_appointment.html', {'service': service})

@login_required
def confirm_booking(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'services/confirm_booking.html', {'appointment': appointment})

@login_required
def complete_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == "POST":
        try:
            Payment.objects.create(
                appointment=appointment,
                amount=appointment.service.price - appointment.reservation_fee,
                is_final=True
            )
            appointment.completed = True
            appointment.save()
            messages.success(request, 'Your payment has been completed successfully.')
            return redirect('thank_you')
        except Exception as e:
            logger.error(f"Error completing payment: {e}")
            messages.error(request, 'There was an error processing your payment. Please try again later.')

    return render(request, 'services/complete_payment.html', {'appointment': appointment})
