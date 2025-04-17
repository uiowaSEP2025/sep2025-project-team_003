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
                org_requester_state = "Iowa",
                org_requester_zip = "52240",
                org_requester_address = "123 main st",
                org_owner_first_name = "Dev",
                org_owner_last_name = "User",
                owning_User = usr,
                org_phone = "1234567890"
                )
            org.save()
            org1 = Organization.objects.create(
                org_name = "testorg",
                org_email = "org1@org1.dev",
                org_city = "Iowa City",
                org_requester_state = "Iowa",
                org_requester_zip = "52240",
                org_requester_address = "123 main st",
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


            for i in range(5):
                c1 = Customer.objects.create(
                    first_name=f"First{i}",
                    last_name=f"Last{i}",
                    email=f"user{i}@example.com",
                    phone_no=f"{random.randint(1000000000, 9999999999)}",
                    notes=f"Sample notes for user {i}",
                    organization=org
                )
                c1.save()

                c2 = Customer.objects.create(
                    first_name=f"First{i}Test",
                    last_name=f"Last{i}Test",
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


            mock_requests = [
                {
                    "requester_first_name": "John",
                    "requester_last_name": "Doe",
                    "requester_email": "johndoe@example.com",
                    "requester_city": "New York",
                    "requester_state": "NY",
                    "requester_zip": "10001",
                    "requester_address": "123 Main St",
                    "requester_phone_no": "1234567890",
                    "description": "Request for plumbing services due to a leaky faucet.",
                    "status": "received",
                },
                {
                    "requester_first_name": "Jane",
                    "requester_last_name": "Smith",
                    "requester_email": "janesmith@example.com",
                    "requester_city": "Los Angeles",
                    "requester_state": "CA",
                    "requester_zip": "90001",
                    "requester_address": "456 Elm St",
                    "requester_phone_no": "9876543210",
                    "description": "Request for electrical repair for faulty wiring.",
                    "status": "approved",
                },
                {
                    "requester_first_name": "Alice",
                    "requester_last_name": "Johnson",
                    "requester_email": "alicej@example.com",
                    "requester_city": "Chicago",
                    "requester_state": "IL",
                    "requester_zip": "60601",
                    "requester_address": "789 Oak St",
                    "requester_phone_no": "5551234567",
                    "description": "Request for HVAC maintenance before winter.",
                    "status": "received",
                },
                {
                    "requester_first_name": "Bob",
                    "requester_last_name": "Brown",
                    "requester_email": "bobbrown@example.com",
                    "requester_city": "Houston",
                    "requester_state": "TX",
                    "requester_zip": "77001",
                    "requester_address": "101 Pine St",
                    "requester_phone_no": "5557654321",
                    "description": "Request for landscaping services for backyard renovation.",
                    "status": "received",
                },
                {
                    "requester_first_name": "Charlie",
                    "requester_last_name": "Davis",
                    "requester_email": "charlied@example.com",
                    "requester_city": "Phoenix",
                    "requester_state": "AZ",
                    "requester_zip": "85001",
                    "requester_address": "202 Maple St",
                    "requester_phone_no": "5559876543",
                    "description": "Request for pest control due to ant infestation.",
                    "status": "approved",
                },
            ]

            for data in mock_requests:
                r = Request.objects.create(
                    requester_first_name=data["requester_first_name"],
                    requester_last_name=data["requester_last_name"],
                    requester_phone_no=data["requester_phone_no"],
                    requester_email=data["requester_email"],
                    requester_city=data["requester_city"],
                    requester_state=data["requester_state"],
                    requester_zip=data["requester_zip"],
                    requester_address=data["requester_address"],
                    description=data["description"],
                    status=data["status"],
                    organization=org,
                )
                r.save()

                r = Request.objects.create(
                    requester_first_name=data["requester_first_name"] + "test",
                    requester_last_name=data["requester_last_name"] + "test",
                    requester_phone_no=data["requester_phone_no"],
                    requester_email=data["requester_email"],
                    requester_city=data["requester_city"],
                    requester_state=data["requester_state"],
                    requester_zip=data["requester_zip"],
                    requester_address=data["requester_address"],
                    description=data["description"],
                    status=data["status"],
                    organization=org1,
                )
                r.save()

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
                    job_city = "Iowa City",
                    job_state = "Iowa",
                    job_zip = "52240",
                    job_address = "2 W Washington St",
                    use_hourly_rate = False,
                    minutes_worked = random.randint(60, 540)
                )
                j.save()

                j = Job.objects.create(
                    job_status=random.choice(['created', 'completed']),
                    start_date=timezone.now().date(),
                    end_date=timezone.now().date() + timezone.timedelta(days=random.randint(1, 30)),
                    description=random.choice(job_descriptions) + " test",
                    organization=org1,
                    customer=customers_1[i],
                    job_city = "Iowa City",
                    job_state = "Iowa",
                    job_zip = "52240",
                    job_address = "2 W Washington St",
                    use_hourly_rate = False,
                    minutes_worked = random.randint(60, 540)
                )
                j.save()


            discount_names = ["Summer Sale", "Black Friday", "Holiday Special", "New Year Discount", "Clearance Sale"]

            for i in range(5):
                d = Discount.objects.create(
                    discount_name=random.choice(discount_names),
                    discount_percent=round(random.uniform(5.0, 50.0)),
                    organization=org
                )
                d.save()

                d = Discount.objects.create(
                    discount_name=random.choice(discount_names) + " test",
                    discount_percent=round(random.uniform(5.0, 50.0)),
                    organization=org1
                )
                d.save()

            jobs_org_1 = Job.objects.filter(organization__pk=org1.pk)[:5]
            jobs_org = Job.objects.filter(organization__pk=org.pk)[:5]
            discounts_1 = Discount.objects.filter(organization__pk=org1.pk)[:5]
            discounts = Discount.objects.filter(organization__pk=org.pk)[:5]

            for i in range(5):
                issuance_date = timezone.now().date()
                due_date = issuance_date + timezone.timedelta(days=30)
                status = 'created' if i % 2 == 0 else 'accepted'
                material_subtotal = 1000.0 * (i + 1)
                total_price = material_subtotal 
                jobID = jobs_org_1[i]

                issuance_date = timezone.now().date()
                due_date = issuance_date + timezone.timedelta(days=30)
                status = 'created' if i % 2 == 0 else 'accepted'
                material_subtotal = 1000.0 * (i + 1)
                total_price = material_subtotal 
                jobID = jobs_org[i]

            # create another job and tie a quote to it
            j = Job.objects.create(
                    job_status=random.choice(['completed']),
                    start_date=timezone.now().date(),
                    end_date=timezone.now().date() + timezone.timedelta(days=random.randint(1, 30)),
                    description=random.choice(job_descriptions),
                    organization=org,
                    customer=customers[1],
                    job_city = "Iowa City",
                    job_state = "Iowa",
                    job_zip = "52240",
                    job_address = "2 W Washington St",
                    use_hourly_rate = True,
                    hourly_rate = random_currency(10, 50),
                    minutes_worked = random.randint(60, 540)
                )
            j.save()


            jobs_for_invoice = Job.objects.filter(
                customer=customers[1],
                job_status="completed",
                quote__status="accepted",  # Ensures only jobs with accepted quotes are selected
                customer__organization=org
            )

            services_org = Service.objects.filter(
                organization = org
            )

            s1, s2 = services_org[:len(services_org) // 2], services_org[len(services_org) // 2:]

            for service in s1:
                js = JobsServices(job=jobs_for_invoice[0], service = service, fee=50)
                js.save()

            for service in s2:
                js = JobsServices(job=jobs_for_invoice[1], service = service, fee=0)
                js.save()

            mats = Material.objects.filter(organization=org)
            m1,m2 = mats[:len(mats) // 2], mats[len(mats) // 2:]
            for m in m1:
                jm = JobsMaterials(
                    unit_price = random_currency(10, 50),
                    quantity = random.randint(1,100),
                    job = jobs_for_invoice[0],
                    material = m
                )
                jm.save()

            for m in m2:
                jm = JobsMaterials(
                    unit_price = random_currency(0, 50),
                    quantity = random.randint(1,100),
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
            
            self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))


        except Exception as e:
            stack_trace = traceback.format_exc()
            self.stdout.write(self.style.ERROR(f'Error seeding the database: {e}\n{stack_trace}'))
        