from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ClientProfile, Service, Appointment, Payment

class UserRegistrationForm(UserCreationForm):
    """
    Form for registering a new user.
    """
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ClientProfileForm(forms.ModelForm):
    """
    Form for creating or updating a client profile.
    """
    class Meta:
        model = ClientProfile
        fields = ['phone_number', 'email', 'address']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'address': forms.Textarea(attrs={'placeholder': 'Address', 'rows': 3}),
        }

class LoginForm(AuthenticationForm):
    """
    Form for user login.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class ServiceForm(forms.ModelForm):
    """
    Form for creating or updating a service offered by the salon.
    """
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Service Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Service Description', 'rows': 4}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price'}),
            'image': forms.ClearableFileInput(attrs={'placeholder': 'Upload Image'}),
        }

class AppointmentForm(forms.ModelForm):
    """
    Form for booking an appointment.
    """
    appointment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Date and Time",
        help_text="Select the date and time for your appointment."
    )

    class Meta:
        model = Appointment
        fields = ['service', 'appointment_date', 'reservation_fee']
        widgets = {
            'reservation_fee': forms.NumberInput(attrs={'placeholder': 'Reservation Fee'}),
        }

    def clean_appointment_date(self):
        # Additional validation can be added here if needed.
        appointment_date = self.cleaned_data.get('appointment_date')
        return appointment_date

class PaymentForm(forms.ModelForm):
    """
    Form for processing a payment.
    """
    class Meta:
        model = Payment
        fields = ['amount', 'payment_type']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Payment Amount'}),
        }
        
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("The payment amount must be positive.")
        return amount
