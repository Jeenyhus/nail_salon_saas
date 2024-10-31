from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    """
    A form for creating new customers
    """
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone']
