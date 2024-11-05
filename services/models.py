from django.utils.text import slugify
from django.db import transaction
from django.db import models
from django.contrib.auth.models import User
import uuid

class ClientProfile(models.Model):
    """
    ClientProfile model represents the profile information of a client in the nail salon application.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model, representing the user associated with this profile.
        phone_number (CharField): An optional field to store the client's contact phone number.
        email (EmailField): An optional field to store the client's contact email address.
        address (TextField): An optional field to store the client's physical address.

    Methods:
        __str__(): Returns the username of the associated user as the string representation of the ClientProfile instance.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Client's contact phone number")
    email = models.EmailField(blank=True, null=True, help_text="Client's contact email")
    address = models.TextField(blank=True, null=True, help_text="Client's address")

    def __str__(self):
        return self.user.username
    
class Service(models.Model):
    """
    A Django model representing a service offered by the nail salon.

    Attributes:
        title (str): The title of the service.
        slug (str): A unique slug for the service, generated from the title.
        description (str): A detailed description of the service.
        price (Decimal): The price of the service.
        image (ImageField): An optional image representing the service.
        created_at (datetime): The date and time when the service was created.
        updated_at (datetime): The date and time when the service was last updated.

    Methods:
        save(*args, **kwargs): Overrides the default save method to generate a slug from the title if it doesn't exist.
        __str__(): Returns the string representation of the service, which is its title.
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Appointment(models.Model):
    """
    Represents an appointment for a service at the nail salon.

    Attributes:
        STATUS_CHOICES (list of tuple): The status options for the appointment.
        client (ForeignKey): The user who made the appointment.
        service (ForeignKey): The service that the appointment is for.
        appointment_date (DateTimeField): The date and time of the appointment.
        status (CharField): The current status of the appointment.
        reservation_fee (DecimalField): The fee for reserving the appointment.
        created_at (DateTimeField): The date and time when the appointment was created.
        updated_at (DateTimeField): The date and time when the appointment was last updated.
        is_deleted (BooleanField): Indicates whether the appointment has been soft deleted.

    Methods:
        __str__(): Returns a string representation of the appointment.
        delete(): Soft deletes the appointment by setting is_deleted to True.
    """
    STATUS_CHOICES = [
        ('reserved', 'Reserved'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='reserved')
    reservation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client.username} - {self.service.title} on {self.appointment_date}"

    def delete(self):
        """Soft delete the appointment by setting is_deleted to True."""
        self.is_deleted = True
        self.save()
    

class Payment(models.Model):
    """
    Represents a payment made for an appointment at the nail salon.
    Attributes:
        PAYMENT_TYPES (list of tuple): The types of payments available.
        appointment (ForeignKey): The appointment associated with the payment.
        amount (DecimalField): The amount of the payment.
        timestamp (DateTimeField): The date and time when the payment was made.
        payment_type (CharField): The type of the payment.
    Methods:
        __str__(): Returns a string representation of the payment.
    """
    PAYMENT_TYPES = [
        ('reservation', 'Reservation'),
        ('final', 'Final'),
        ('installment', 'Installment'),
    ]
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    
    def __str__(self):
        return f"Payment of {self.amount} for {self.appointment}"

class Notification(models.Model):
    """
    Represents a notification reminder for an appointment.

    Attributes:
        REMINDER_TYPES (list of tuple): The types of reminders available.
        appointment (ForeignKey): The appointment associated with the reminder.
        reminder_type (CharField): The type of the reminder (email or SMS).
        reminder_date (DateTimeField): The date and time when the reminder should be sent.
        sent (BooleanField): Indicates whether the reminder has been sent.

    Methods:
        __str__(): Returns a string representation of the notification.
    """
    REMINDER_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
    ]
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    reminder_type = models.CharField(max_length=10, choices=REMINDER_TYPES)
    reminder_date = models.DateTimeField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reminder_type.capitalize()} reminder for {self.appointment}"


def create_appointment_with_initial_payment(client, service, appointment_date, reservation_fee):
    """
    Creates an appointment with an initial reservation payment.

    Args:
        client (User): The user who is making the appointment.
        service (Service): The service for which the appointment is being made.
        appointment_date (datetime): The date and time of the appointment.
        reservation_fee (Decimal): The fee for reserving the appointment.

    Returns:
        Appointment: The created appointment instance.
    """
    with transaction.atomic():
        appointment = Appointment.objects.create(
            client=client,
            service=service,
            appointment_date=appointment_date,
            reservation_fee=reservation_fee,
            status='reserved'
        )
        Payment.objects.create(
            appointment=appointment,
            amount=reservation_fee,
            payment_type='reservation'
        )
    return appointment