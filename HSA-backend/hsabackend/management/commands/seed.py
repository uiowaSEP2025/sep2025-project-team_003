from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from hsabackend.models.customer import Customer
from hsabackend.models.contractor import Contractor
from hsabackend.models.material import Material
from django.contrib.auth.models import User
from hsabackend.models.request import Request
from hsabackend.models.job import Job, JobsMaterials, JobsServices
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.discount import Discount
from django.utils import timezone
import traceback

import random

from hsabackend.serializers.contractor_serializer import ContractorSerializer
from hsabackend.serializers.customer_serializer import CustomerSerializer
from hsabackend.serializers.discount_serializer import DiscountSerializer
from hsabackend.serializers.job_serializer import JobSerializer
from hsabackend.serializers.material_serializer import MaterialSerializer
from hsabackend.serializers.organization_serializer import OrganizationSerializer
from hsabackend.serializers.service_serializer import ServiceSerializer


def random_currency(min_value=0.01, max_value=1000.00):
    """
    Generate a random currency value within a given range.
    
    :param min_value: Minimum currency value (default is 0.01)
    :param max_value: Maximum currency value (default is 1000.00)
    :return: A formatted string representing the random currency value
    """
    return round(random.uniform(min_value, max_value), 2)

class Command(BaseCommand):
    """seeds the database with test data. DO NOT RUN ON PROD! Is non-deterministic!!!!"""

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
            User.objects.create_user("testuser", "test@uiowa.edu", "SepTeam003!")
            usr  = User.objects.first()
            usr1  = User.objects.last()
            usr.save()
            usr1.save()

            org_data_1 = {
                "org_name"              : "devorg",
                "org_email"             : "org@org.dev",
                "org_city"              : "Iowa City",
                "org_state"             : "Iowa",
                "org_zip"               : "52240",
                "org_address"           : "123 main st",
                "org_owner_first_name"  : "Dev",
                "org_owner_last_name"   : "User",
                "owning_user"           : usr,
                "org_phone"             : "1234567890",
                "is_onboarding"         : False,
                "default_labor_rate"    : random_currency(100,150),
                "default_payment_link"  : "https://www.paypal.com"
            }
            org_serializer_1 = OrganizationSerializer(data=org_data_1)
            org_serializer_1.is_valid(raise_exception=True)
            org_serializer_1.create(org_data_1)

            org_data_2 = {
                "org_name"              : "testorg",
                "org_email"             : "org1@org.dev",
                "org_city"              : "Iowa City",
                "org_state"             : "Iowa",
                "org_zip"               : "52240",
                "org_address"           : "123 main st",
                "org_owner_first_name"  : "Test",
                "org_owner_last_name"   : "User",
                "owning_user"           : usr1,
                "org_phone"             : "1234567890",
                "is_onboarding"         : False,
                "default_labor_rate"    : random_currency(100, 150),
                "default_payment_link"  : "https://www.paypal.com"
            }
            org_serializer_2 = OrganizationSerializer(data=org_data_2)
            org_serializer_2.is_valid(raise_exception=True)
            org_serializer_2.create(org_data_2)
            
            org_1 = Organization.objects.filter(owning_user=usr.id).first()
            org_2 = Organization.objects.filter(owning_user=usr1.id).first()
            
            service_data = [
                {"service_name": "Window Cleaning",
                 "service_description": "Cleaning of windows for residential and commercial properties.",
                 "default_fee": 0,
                 "organization": org_1},
                {"service_name": "Pest Control",
                 "service_description": "Extermination and prevention of pests.",
                 "default_fee": 0},
                {"service_name": "Handyman Services",
                 "service_description": "General repair and maintenance services.",
                 "default_fee": 0,
                 "organization": org_1},
                ]
            
            service_data1 = [
                {"service_name": "Window Cleaning",
                 "service_description": "Cleaning of windows for residential and commercial properties. (test user)",
                 "default_fee": 0,
                 "organization": org_2},
                {"service_name": "Pest Control",
                 "service_description": "Extermination and prevention of pests. (test user)",
                 "default_fee": 0,
                 "organization": org_2},
                {"service_name": "Handyman Services",
                 "service_description": "General repair and maintenance services. (test user)",
                 "default_fee": 0,
                 "organization": org_2},
                ]

            # Create services in a loop
            for data in service_data:
                service_serializer = ServiceSerializer(data=data)
                service_serializer.is_valid(raise_exception=True)
                service_serializer.create(data)

            for data in service_data1:
                service_serializer = ServiceSerializer(data=data)
                service_serializer.is_valid(raise_exception=True)
                service_serializer.create(data)


            for i in range(5):
                customer_data = {
                    "first_name": f"First{i}",
                    "last_name": f"Last{i}",
                    "email": f"user{i}@example.com",
                    "phone": f"{random.randint(1000000000, 9999999999)}",
                    "notes": f"Sample notes for user {i}",
                    "organization": org_1
                }

                customer_data_2 = {
                    "first_name": f"First{i}",
                    "last_name": f"Last{i}",
                    "email": f"user{i}@example.com",
                    "phone": f"{random.randint(1000000000, 9999999999)}",
                    "notes": f"Sample notes for user {i}",
                    "organization": org_2
                }

                customerserializer = CustomerSerializer(data=customer_data)
                customerserializer.is_valid(raise_exception=True)
                customerserializer.create(customer_data)
                customerserializer2 = CustomerSerializer(data=customer_data_2)
                customerserializer2.is_valid(raise_exception=True)
                customerserializer2.create(customer_data)

                contractor_data = {
                    "first_name": f"First{i}Con",
                    "last_name": f"Last{i}Con",
                    "email": f"con{i}@example.com",
                    "phone": f"{random.randint(1000000000, 9999999999)}",
                    "organization": org_1
                }

                contractor_data_2 = {
                    "first_name": f"First{i}Con",
                    "last_name": f"Last{i}Con",
                    "email": f"con{i}@example.com",
                    "phone": f"{random.randint(1000000000, 9999999999)}",
                    "organization": org_2
                }
                contractor_serializer = ContractorSerializer(data=contractor_data)
                contractor_serializer.is_valid(raise_exception=True)
                contractor_serializer.create(contractor_data)
                contractor_serializer2 = ContractorSerializer(data=contractor_data_2)
                contractor_serializer2.is_valid(raise_exception=True)
                contractor_serializer2.create(contractor_data)

            material_names = [
                "Steel Beam",
                "Concrete Mix",
                "Aluminum Sheet",
                "Copper Wire",
                "PVC Pipe",
            ]

            for i in range(5):
                material_data = {
                    "material_name": f"{material_names[i]} devuser",
                    "material_description": f"Sample description for {material_names[i]}",
                    "default_cost": random_currency(1,500),
                    "organization": org_1
                }
                material_data_2 = {
                    "material_name": f"{material_names[i]} testuser",
                    "material_description": f"Sample description for {material_names[i]} (test user)",
                    "default_cost": random_currency(1,500),
                    "organization": org_2
                }
                material_serializer = MaterialSerializer(data=material_data)
                material_serializer.is_valid(raise_exception=True)
                material_serializer.create(material_data)
                material_serializer2 = MaterialSerializer(data=material_data_2)
                material_serializer2.is_valid(raise_exception=True)
                material_serializer2.create(material_data_2)


            mock_requests_data_1 = [
                {
                    "requester_first_name": "John",
                    "requester_last_name": "Doe",
                    "requester_email": "johndoe@example.com",
                    "requester_city": "New York",
                    "requester_state": "NY",
                    "requester_zip": "10001",
                    "requester_address": "123 Main St",
                    "requester_phone": "1234567890",
                    "availability": "M-F afternoons",
                    "description": "Request for plumbing services due to a leaky faucet.",
                    "request_status": "received",
                    "organization": org_1
                },
                {
                    "requester_first_name": "Jane",
                    "requester_last_name": "Smith",
                    "requester_email": "janesmith@example.com",
                    "requester_city": "Los Angeles",
                    "requester_state": "CA",
                    "requester_zip": "90001",
                    "requester_address": "456 Elm St",
                    "requester_phone": "9876543210",
                    "availability": "M-F mornings",
                    "description": "Request for electrical repair for faulty wiring.",
                    "request_status": "approved",
                    "organization": org_1
                },
                {
                    "requester_first_name": "Alice",
                    "requester_last_name": "Johnson",
                    "requester_email": "alicej@example.com",
                    "requester_city": "Chicago",
                    "requester_state": "IL",
                    "requester_zip": "60601",
                    "requester_address": "789 Oak St",
                    "requester_phone": "5551234567",
                    "availability": "Weekends anytime",
                    "description": "Request for HVAC maintenance before winter.",
                    "request_status": "received",
                    "organization": org_1
                },
                {
                    "requester_first_name": "Bob",
                    "requester_last_name": "Brown",
                    "requester_email": "bobbrown@example.com",
                    "requester_city": "Houston",
                    "requester_state": "TX",
                    "requester_zip": "77001",
                    "requester_address": "101 Pine St",
                    "requester_phone": "5557654321",
                    "availability": "Weekdays in the evening",
                    "description": "Request for landscaping services for backyard renovation.",
                    "request_status": "received",
                    "organization": org_1
                },
                {
                    "requester_first_name": "Charlie",
                    "requester_last_name": "Davis",
                    "requester_email": "charlied@example.com",
                    "requester_city": "Phoenix",
                    "requester_state": "AZ",
                    "requester_zip": "85001",
                    "requester_address": "202 Maple St",
                    "requester_phone": "5559876543",
                    "availability": "Weekends in the mornings",
                    "description": "Request for pest control due to ant infestation.",
                    "request_status": "approved",
                    "organization": org_1
                },
            ]

            mock_requests_data_2 = [
                {
                    "requester_first_name": "John",
                    "requester_last_name": "Doe",
                    "requester_email": "johndoe@example.com",
                    "requester_city": "New York",
                    "requester_state": "NY",
                    "requester_zip": "10001",
                    "requester_address": "123 Main St",
                    "requester_phone": "1234567890",
                    "availability": "M-F afternoons",
                    "description": "Request for plumbing services due to a leaky faucet.",
                    "request_status": "received",
                    "organization": org_2
                },
                {
                    "requester_first_name": "Jane",
                    "requester_last_name": "Smith",
                    "requester_email": "janesmith@example.com",
                    "requester_city": "Los Angeles",
                    "requester_state": "CA",
                    "requester_zip": "90001",
                    "requester_address": "456 Elm St",
                    "requester_phone": "9876543210",
                    "availability": "M-F mornings",
                    "description": "Request for electrical repair for faulty wiring.",
                    "request_status": "approved",
                    "organization": org_2
                },
                {
                    "requester_first_name": "Alice",
                    "requester_last_name": "Johnson",
                    "requester_email": "alicej@example.com",
                    "requester_city": "Chicago",
                    "requester_state": "IL",
                    "requester_zip": "60601",
                    "requester_address": "789 Oak St",
                    "requester_phone": "5551234567",
                    "availability": "Weekends anytime",
                    "description": "Request for HVAC maintenance before winter.",
                    "request_status": "received",
                    "organization": org_2
                },
                {
                    "requester_first_name": "Bob",
                    "requester_last_name": "Brown",
                    "requester_email": "bobbrown@example.com",
                    "requester_city": "Houston",
                    "requester_state": "TX",
                    "requester_zip": "77001",
                    "requester_address": "101 Pine St",
                    "requester_phone": "5557654321",
                    "availability": "Weekdays in the evening",
                    "description": "Request for landscaping services for backyard renovation.",
                    "request_status": "received",
                    "organization": org_2
                },
                {
                    "requester_first_name": "Charlie",
                    "requester_last_name": "Davis",
                    "requester_email": "charlied@example.com",
                    "requester_city": "Phoenix",
                    "requester_state": "AZ",
                    "requester_zip": "85001",
                    "requester_address": "202 Maple St",
                    "requester_phone": "5559876543",
                    "availability": "Weekends in the mornings",
                    "description": "Request for pest control due to ant infestation.",
                    "request_status": "approved",
                    "organization": org_2
                },
            ]


                        # List of realistic job descriptions
            job_descriptions = [
                "Install new HVAC system in the office building.",
                "Repair the plumbing system in the residential complex.",
                "Landscaping and garden maintenance for the corporate park.",
                "Electrical wiring upgrade for the warehouse.",
                "Painting and interior decoration for the new showroom.",
            ]

            services_1 = Service.objects.filter(organization=org_1).all()
            services_2 = Service.objects.filter(organization=org_2).all()
            materials_1 = Material.objects.filter(organization=org_1).all()
            materials_2 = Material.objects.filter(organization=org_2).all()

            # Generate 5 mock Job instances
            for i in range(5):

                service_seed_1 = random.choice(services_1)
                service_seed_2 = random.choice(services_2)
                material_seed_1 = random.choice(materials_1)
                material_seed_2 = random.choice(materials_2)


                job_data = {
                    "job_status": random.choice(['created', 'accepted', 'completed']),
                    "start_date": timezone.now().date(),
                    "end_date": timezone.now().date() + timezone.timedelta(days=random.randint(1, 30)),
                    "description": random.choice(job_descriptions),
                    "organization": org_1,
                    "job_city": mock_requests_data_1[i]["requester_city"],
                    "job_state": mock_requests_data_1[i]["requester_state"],
                    "job_zip": mock_requests_data_1[i]["requester_zip"],
                    "job_address": mock_requests_data_1[i]["requester_address"],
                    "use_hourly_rate": True,
                    "minutes_worked": random.randint(60, 540),
                    "hourly_rate": random_currency(10, 50),
                    "services": [service_seed_1],
                    "materials": [material_seed_1]
                }

                job_data_2 = {
                    "job_status": random.choice(['created', 'accepted', 'completed']),
                    "start_date": timezone.now().date(),
                    "end_date": timezone.now().date() + timezone.timedelta(days=random.randint(1, 30)),
                    "description": random.choice(job_descriptions),
                    "organization": org_2,
                    "job_city": mock_requests_data_2[i]["requester_city"],
                    "job_state": mock_requests_data_2[i]["requester_state"],
                    "job_zip": mock_requests_data_2[i]["requester_zip"],
                    "job_address": mock_requests_data_2[i]["requester_address"],
                    "use_hourly_rate": True,
                    "minutes_worked": random.randint(60, 540),
                    "hourly_rate": random_currency(10, 50),
                    "services": [service_seed_2],
                    "materials": [material_seed_2]
                }

                job_serializer = JobSerializer(data=job_data)
                job_serializer.is_valid(raise_exception=True)
                job_serializer.create(job_data)
                job_serializer2 = JobSerializer(data=job_data_2)
                job_serializer2.is_valid(raise_exception=True)
                job_serializer2.create(job_data_2)




            discount_names = ["Summer Sale", "Black Friday", "Holiday Special", "New Year Discount", "Clearance Sale"]

            for i in range(5):
                discount_data = {
                    "discount_name": random.choice(discount_names),
                    "discount_percent": round(random.uniform(5.0, 50.0)),
                    "organization": org_1
                }

                discount_data_2 = {
                    "discount_name": random.choice(discount_names),
                    "discount_percent": round(random.uniform(5.0, 50.0)),
                    "organization": org_2
                }
                discount_serializer = DiscountSerializer(data=discount_data)
                discount_serializer.is_valid(raise_exception=True)
                discount_serializer.create(discount_data)
                discount_serializer2 = DiscountSerializer(data=discount_data_2)
                discount_serializer2.is_valid(raise_exception=True)
                discount_serializer2.create(discount_data_2)

            self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))


        except Exception as e:
            stack_trace = traceback.format_exc()
            self.stdout.write(self.style.ERROR(f'Error seeding the database: {e}\n{stack_trace}'))
        