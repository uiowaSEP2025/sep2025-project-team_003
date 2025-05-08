from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from hsabackend.models.customer import Customer
from hsabackend.models.contractor import Contractor
from hsabackend.models.material import Material
from django.contrib.auth.models import User
from hsabackend.models.request import Request
from hsabackend.models.job_service import JobService
from hsabackend.models.job import Job
from hsabackend.models.discount_type import DiscountType
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.subscription import Subscription
from django.utils import timezone
import traceback
from hsabackend.models.job_material import JobMaterial

import random


def random_currency(min_value=0.01, max_value=1000.00):
    """
    Generate a random currency value within a given range.
    
    :param min_value: Minimum currency value (default is 0.01)
    :param max_value: Maximum currency value (default is 1000.00)
    :param currency_symbol: Currency symbol to prefix (default is "$")
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
            
            org = Organization.objects.create(
                org_name = "devorg",
                org_email = "org@org.dev",
                org_city = "Iowa City",
                org_requestor_state = "Iowa",
                org_requestor_zip = "52240",
                org_requestor_address = "123 main st",
                org_owner_first_name = "Dev",
                org_owner_last_name = "User",
                owning_User = usr,
                org_phone = "1234567890",
                is_onboarding = False,
                )
            org.save()
            org1 = Organization.objects.create(
                org_name = "testorg",
                org_email = "org1@org1.dev",
                org_city = "Iowa City",
                org_requestor_state = "Iowa",
                org_requestor_zip = "52240",
                org_requestor_address = "123 main st",
                org_owner_first_name = "Test",
                org_owner_last_name = "User",
                owning_User = usr1,
                org_phone = "1234567890"
                )
            org1.save()
            
            service_data = [
                {"name": "Window Cleaning", "description": "Cleaning of windows for residential and commercial properties."},
                {"name": "Pest Control", "description": "Extermination and prevention of pests."},
                {"name": "Handyman Services", "description": "General repair and maintenance services."},
                ]
            
            service_data1 = [
                {"name": "Window Cleaning", "description": "Cleaning of windows for residential and commercial properties. (test user)"},
                {"name": "Pest Control", "description": "Extermination and prevention of pests. (test user)"},
                {"name": "Handyman Services", "description": "General repair and maintenance services. (test user)"},
                ]

            # Create services in a loop
            for data in service_data:
                s1 = Service.objects.create(
                    service_name=data["name"],
                    service_description=data["description"],
                    organization=org
                )
                s1.save

            for data in service_data1:
                s2 = Service.objects.create(
                    service_name=data["name"],
                    service_description=data["description"],
                    organization=org1
                )
                s2.save


            first_names = ["Alice", "Bob", "Charlie", "Diana", "Ethan"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Davis"]


            for i in range(5):
                c1 = Customer.objects.create(
                    first_name=random.choice(first_names),
                    last_name=f"Last{i}",
                    email=f"user{i}@example.com",
                    phone_no=f"{random.randint(1000000000, 9999999999)}",
                    notes=f"Sample notes for user {i}",
                    organization=org
                )
                c1.save()

                c2 = Customer.objects.create(
                    first_name=random.choice(first_names) + "test",
                    last_name=random.choice(last_names) + "test",
                    email=f"testuser{i}@example.com",
                    phone_no=f"{random.randint(1000000000, 9999999999)}",
                    notes=f"Sample notes for test user {i}",
                    organization=org1
                )
                c2.save()

                customers = Customer.objects.filter(organization=org.pk)
                customers_1 = Customer.objects.filter(organization=org.pk)
            
            for i in range(5):
                con1 = Contractor.objects.create(
                    first_name=f"First{i}Con",
                    last_name=f"Last{i}Con",
                    email=f"con{i}@example.com",
                    phone=f"{random.randint(1000000000, 9999999999)}",
                    organization=org
                )
                con1.save()

                con2 = Contractor.objects.create(
                    first_name=f"First{i}ConTest",
                    last_name=f"Last{i}ConTest",
                    email=f"testcon{i}@example.com",
                    phone=f"{random.randint(1000000000, 9999999999)}",
                    organization=org1
                )
                con2.save()

                contractors = Contractor.objects.filter(organization=org.pk)
                contractors_1 = Contractor.objects.filter(organization=org.pk)

            material_names = [
                "Steel Beam",
                "Concrete Mix",
                "Aluminum Sheet",
                "Copper Wire",
                "PVC Pipe",
            ]

            for i in range(5):
                m = Material.objects.create(
                    material_name=material_names[i],   
                    organization=org  # Cycle through organizations
                )
                m.save()

                m1 = Material.objects.create(
                    material_name=f"{material_names[i]} testuser",   
                    organization=org1 # Cycle through organizations
                )
                m1.save()


        
                        # List of realistic job descriptions
            job_descriptions = [
                "Install new HVAC system in the office building.",
                "Repair the plumbing system in the residential complex.",
                "Landscaping and garden maintenance for the corporate park.",
                "Electrical wiring upgrade for the warehouse.",
                "Painting and interior decoration for the new showroom.",
            ]

            # Generate 5 mock Job instances
            for i in range(5):
                j = Job.objects.create(
                    job_status=random.choice(['completed']),
                    start_date=timezone.now().date(),
                    end_date=timezone.now().date() + timezone.timedelta(days=random.randint(1, 30)),
                    description=random.choice(job_descriptions),
                    organization=org,
                    customer=customers[i],
                    requestor_city = "Iowa City",
                    requestor_state = "Iowa",
                    requestor_zip = "52240",
                    requestor_address = "2 W Washington St",
                    flat_fee = 0.00,
                    hourly_rate = 50.00,
                    minutes_worked = 100
                )
                j.save()

                j = Job.objects.create(
                    job_status=random.choice(['created', 'completed']),
                    start_date=timezone.now().date(),
                    end_date=timezone.now().date() + timezone.timedelta(days=random.randint(1, 30)),
                    description=random.choice(job_descriptions) + " test",
                    organization=org1,
                    customer=customers_1[i],
                    requestor_city = "Iowa City",
                    requestor_state = "Iowa",
                    requestor_zip = "52240",
                    requestor_address = "2 W Washington St",
                    flat_fee = 0.00,
                    hourly_rate = 50.00,
                    minutes_worked = 100
                )
                j.save()

            j1 = Job.objects.filter(organization=org)
            j2 = Job.objects.filter(organization=org1)

            Request.objects.create(
            requester_first_name="John",
            requester_last_name="Doe",
            requester_email="john.doe@example.com",
            requester_city="Springfield",
            requester_state="CA",
            requester_zip="12345",
            requester_address="123 Elm St",
            requester_phone="1234567890",
            description="Need help fixing kitchen sink",
            availability="Weekends",
            request_status="received",
            organization=org,
            job=j1[0]
        )

            Request.objects.create(
                requester_first_name="Jane",
                requester_last_name="Smith",
                requester_email="jane.smith@example.com",
                requester_city="Springfield",
                requester_state="CA",
                requester_zip="12345",
                requester_address="456 Oak St",
                requester_phone="0987654321",
                description="Need someone to repair bathroom faucet",
                availability="Weekdays after 5pm",
                request_status="approved",
                organization=org1,
                job=j2[0]
            )


            discount_names = ["Summer Sale", "Black Friday", "Holiday Special", "New Year Discount", "Clearance Sale"]

            for i in range(5):
                d = DiscountType.objects.create(
                    discount_name=random.choice(discount_names),
                    discount_percent=round(random.uniform(5.0, 50.0)),
                    organization=org
                )
                d.save()

                d = DiscountType.objects.create(
                    discount_name=random.choice(discount_names) + " test",
                    discount_percent=round(random.uniform(5.0, 50.0)),
                    organization=org1
                )
                d.save()

            jobs_org_1 = Job.objects.filter(organization__pk=org1.pk)[:5]
            jobs_org = Job.objects.filter(organization__pk=org.pk)[:5]
            discounts_1 = DiscountType.objects.filter(organization__pk=org1.pk)[:5]
            discounts = DiscountType.objects.filter(organization__pk=org.pk)[:5]

            
            # create another job and tie a quote to it
            j = Job.objects.create(
                    job_status=random.choice(['completed']),
                    start_date=timezone.now().date(),
                    end_date=timezone.now().date() + timezone.timedelta(days=random.randint(1, 30)),
                    description=random.choice(job_descriptions),
                    organization=org,
                    customer=customers[1],
                    requestor_city = "Iowa City",
                    requestor_state = "Iowa",
                    requestor_zip = "52240",
                    requestor_address = "2 W Washington St",
                    flat_fee = 0.00,
                    hourly_rate = 50.00,
                    minutes_worked = 100
                )
            j.save()


            jobs_for_invoice = Job.objects.filter(
                customer=customers[1],
                job_status="completed",
                customer__organization=org
            )

            services_org = Service.objects.filter(
                organization = org
            )

            s1, s2 = services_org[:len(services_org) // 2], services_org[len(services_org) // 2:]

            for service in s1:
                js = JobService(job=jobs_for_invoice[0], service = service)
                js.save()

            for service in s2:
                js = JobService(job=jobs_for_invoice[1], service = service)
                js.save()

            mats = Material.objects.filter(organization=org)
            m1,m2 = mats[:len(mats) // 2], mats[len(mats) // 2:]
            for m in m1:
                jm = JobMaterial(
                    price_per_unit = random_currency(10, 50),
                    units_used = random.randint(1,100),
                    job = jobs_for_invoice[0],
                    material = m
                )
                jm.save()

            for m in m2:
                jm = JobMaterial(
                    price_per_unit = random_currency(0, 50),
                    units_used = random.randint(1,100),
                    job = jobs_for_invoice[1],
                    material = m
                )
                jm.save()

            

            for i in range(5):
                j = JobTemplate.objects.create(
                    description=f"Job Template Description {i+1}",
                    name=f"Template {i+1}",
                    organization=org)
                j.save()
                j = JobTemplate.objects.create(
                    description=f"Job Template Description {i+1}",
                    name=f"Template {i+1}",
                    organization=org1)
                j.save()
            
            job_templates = JobTemplate.objects.filter(organization=org.pk)[:5]
            job_templates_1 = JobTemplate.objects.filter(organization=org.pk)[:5]
            for i in range(5):
                Subscription.objects.create(
                    description=f"Sample Job Description {i+1}",
                    price=100.0 * (i + 1),
                    job_template=job_templates[i]
                ).save()
                Subscription.objects.create(
                    description=f"Sample Job Description {i+1}",
                    price=100.0 * (i + 1),
                    job_template=job_templates_1[i]
                ).save()

            
            self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))


        except Exception as e:
            stack_trace = traceback.format_exc()
            self.stdout.write(self.style.ERROR(f'Error seeding the database: {e}\n{stack_trace}'))
        