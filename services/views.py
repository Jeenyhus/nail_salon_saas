from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse
from .models import Service, Appointment, Payment
from .forms import AppointmentForm, ServiceForm, PaymentForm
# Login and logout views
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm


def is_admin(user):
    """
    Check if the given user belongs to the 'Admin' group.

    Args:
        user (User): The user object to check.

    Returns:
        bool: True if the user is an admin, False otherwise.

    Example:
        >>> user = User.objects.get(username='john_doe')
        >>> is_admin(user)
        True
    """
    return user.groups.filter(name='Admin').exists()


def home(request):
    """
    Renders the home page with a list of all services.

    This view function retrieves all Service objects from the database
    and passes them to the 'home.html' template for rendering.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'home.html' template with the list of services.

    """
    services = Service.objects.all()
    return render(request, 'home.html', {'services': services})


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class ServiceListView(ListView):
    """
    View to list all services.

    This view is restricted to admin users only. It retrieves all Service objects
    from the database and passes them to the 'service_list.html' template for rendering.

    Attributes:
        model (Model): The model that this view will operate upon.
        template_name (str): The name of the template to render.
        context_object_name (str): The context variable name to use for the list of services.
    """
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class ServiceCreateView(View):
    """
    View to create a new service.

    This view is restricted to admin users only. It handles both GET and POST requests
    to display a form for creating a new Service and to process the form submission.

    Methods:
        get(request): Handles GET requests to display the service creation form.
        post(request): Handles POST requests to process the service creation form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered template for the service creation form or a redirect to the service list.
    """
    def get(self, request):
        form = ServiceForm()
        return render(request, 'service_form.html', {'form': form})
    
    def post(self, request):
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service created successfully.")
            return redirect('service_list')
        return render(request, 'service_form.html', {'form': form})


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class ServiceUpdateView(View):
    """
    View for updating a service.
    Requires user to be logged in and to pass an admin test.
    """

    def get(self, request, pk):
        """
        Handles GET requests to display the service update form.
        Fetches the service instance based on the primary key (pk) and initializes the form.
        """
        service = get_object_or_404(Service, pk=pk)
        form = ServiceForm(instance=service)
        return render(request, 'service_form.html', {'form': form})
    
    def post(self, request, pk):
        """
        Handles POST requests to update the service with the provided data.
        Validates the form, saves the updated service, and redirects to the service list.
        Displays a success message upon successful update.
        """
        service = get_object_or_404(Service, pk=pk)
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully.")
            return redirect('service_list')
        return render(request, 'service_form.html', {'form': form})


@login_required
def appointment_create(request, service_id):
    """
    View for creating a new appointment for a specific service.
    Requires the user to be logged in. If the request method is POST, validates the form
    and saves the appointment. Redirects to the client dashboard on success.
    """
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.client = request.user
            appointment.service = service
            appointment.save()
            messages.success(request, "Appointment booked successfully.")
            return redirect('client_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'appointment_form.html', {'form': form, 'service': service})

@login_required
def payment_create(request, appointment_id):
    """
    View for processing payment for a specific appointment.
    Requires the user to be logged in. Validates the payment form and associates it with the appointment.
    Redirects to the client dashboard upon successful payment processing.
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.appointment = appointment
            payment.save()
            messages.success(request, "Payment processed successfully.")
            return redirect('client_dashboard')
    else:
        form = PaymentForm()
    return render(request, 'payment_form.html', {'form': form, 'appointment': appointment})


@login_required
def client_dashboard(request):
    """
    View for displaying the client's dashboard with their appointments.
    Fetches all appointments for the logged-in user that are not deleted,
    ordered by appointment date in descending order.
    """
    appointments = Appointment.objects.filter(client=request.user, is_deleted=False).order_by('-appointment_date')
    return render(request, 'client_dashboard.html', {'appointments': appointments})



def login_view(request):
    """
    View for handling user login.
    Displays the login form and authenticates the user upon valid submission.
    Redirects to the home page on successful login; displays an error message on failure.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    """
    View for logging out the user.
    Clears the session and redirects to the home page.
    """
    logout(request)
    return redirect('home')