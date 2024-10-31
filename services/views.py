from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Service

class ServiceListView(ListView):
    """
    View to list all services.
    """
    model = Service
    template_name = "services/service_list.html"
    context_object_name = "services"


class ServiceDetailView(DetailView):
    """
    View to display details of a single service.
    """
    model = Service
    template_name = "services/service_detail.html"
    context_object_name = "service"


class ServiceCreateView(CreateView):
    """
    View to create a new service.
    """
    model = Service
    fields = ['name', 'description', 'price', 'duration']
    template_name = "services/service_form.html"
    success_url = reverse_lazy('service_list')


class ServiceUpdateView(UpdateView):
    """
    View to update an existing service.
    """
    model = Service
    fields = ['name', 'description', 'price', 'duration']
    template_name = "services/service_form.html"
    success_url = reverse_lazy('service_list')
