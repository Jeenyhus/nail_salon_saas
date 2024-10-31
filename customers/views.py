from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Customer, CustomerInteraction

class CustomerListView(ListView):
    """
    View to list all customers.
    """
    model = Customer
    template_name = "customers/customer_list.html"
    context_object_name = "customers"


class CustomerDetailView(DetailView):
    """
    View to display details of a single customer.
    """
    model = Customer
    template_name = "customers/customer_detail.html"
    context_object_name = "customer"

    def get_context_data(self, **kwargs):
        """
        Add customer interactions to the context.
        """
        context = super().get_context_data(**kwargs)
        context['interactions'] = CustomerInteraction.objects.filter(customer=self.object)
        return context


class CustomerCreateView(CreateView):
    """
    View to create a new customer.
    """
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy('customer_list')


class CustomerUpdateView(UpdateView):
    """
    View to update an existing customer.
    """
    model = Customer
    fields = ['first_name', 'last_name', 'email', 'phone']
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy('customer_list')
