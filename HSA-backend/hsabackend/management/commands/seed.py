from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from hsabackend.models.customer import Customer
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    """seeds the database with test data. DO NOT RUN ON PROD!"""

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.NOTICE('About to seed the database')
        )
        try:
            call_command('flush', interactive=False) # truncates all tables
            self.stdout.write(self.style.SUCCESS('Database flushed successfully'))
        except CommandError as e:
            self.stdout.write(self.style.ERROR(f'Error flushing the database: {e}'))
        try: 
            User.objects.create_user("devuser", "dev@uiowa.edu", "SepTeam003!")
            usr  = User.objects.first()
            org = Organization.objects.create(
                org_name = "org1",
                org_email = "org1@org1.dev",
                org_city = "Iowa City",
                org_requestor_state = "IA",
                org_requestor_zip = "52240",
                org_requestor_address = "123 main st",
                org_owner_first_name = "Dev",
                org_owner_last_name = "User",
                owning_User = usr
                )
            org.save()
            
            service_data = [
                {"name": "Window Cleaning", "description": "Cleaning of windows for residential and commercial properties."},
                {"name": "Pest Control", "description": "Extermination and prevention of pests."},
                {"name": "Handyman Services", "description": "General repair and maintenance services."},
    ]

            # Create services in a loop
            for data in service_data:
                Service.objects.create(
                    service_name=data["name"],
                    service_description=data["description"],
                    organization=org
                )

            for i in range(5):
                Customer.objects.create(
                    first_name=f"First{i}",
                    last_name=f"Last{i}",
                    email=f"user{i}@example.com",
                    phone_no=f"{random.randint(1000000000, 9999999999)}",
                    notes=f"Sample notes for user {i}",
                    organization=org
                )


        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding the database: {e}'))
        