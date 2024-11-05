import requests
from django.core.management.base import BaseCommand
from services.models import Service
from django.core.files.base import ContentFile
from io import BytesIO
import random

class Command(BaseCommand):
    help = 'Populate the database with dummy services and images from online sources.'

    # List of sample service titles, descriptions, and image URLs
    SAMPLE_SERVICES = [
        ("Basic Manicure", "A classic manicure that includes nail shaping, cuticle care, and a polish of your choice.", "https://via.placeholder.com/300x200.png?text=Basic+Manicure"),
        ("Gel Manicure", "A gel-based manicure for a long-lasting and glossy finish.", "https://via.placeholder.com/300x200.png?text=Gel+Manicure"),
        ("Spa Pedicure", "A relaxing pedicure experience with a soothing foot soak, exfoliation, and massage.", "https://via.placeholder.com/300x200.png?text=Spa+Pedicure"),
        ("Acrylic Nails", "Customizable acrylic nail extensions for length and durability.", "https://via.placeholder.com/300x200.png?text=Acrylic+Nails"),
        ("Nail Art", "Creative nail art design to make your nails stand out.", "https://via.placeholder.com/300x200.png?text=Nail+Art"),
    ]

    def handle(self, *args, **options):
        # Clear existing data for a clean start
        Service.objects.all().delete()
        print("Cleared existing services.")

        for title, description, image_url in self.SAMPLE_SERVICES:
            # Randomly generate a price between 10 and 100
            price = round(random.uniform(10, 100), 2)

            # Download the image from the URL
            image = self.download_image(image_url)

            # Create and save the service instance
            service = Service(title=title, description=description, price=price)
            service.image.save(f'{title.lower().replace(" ", "_")}.png', image, save=True)
            service.save()

            print(f"Added service: {title}")

    def download_image(self, url):
        """Downloads an image from the given URL and returns a ContentFile."""
        response = requests.get(url)
        if response.status_code == 200:
            return ContentFile(response.content)
        else:
            print(f"Failed to download image from {url}")
            return ContentFile(b'')  # Return an empty ContentFile if the download fails
