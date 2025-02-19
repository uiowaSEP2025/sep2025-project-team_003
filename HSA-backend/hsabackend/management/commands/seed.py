from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from hsabackend.models.organization import Organization
from hsabackend.models.service import Service
from hsabackend.models.customer import Customer
from hsabackend.models.material import Material
from django.contrib.auth.models import User
from hsabackend.models.request import Request
from hsabackend.models.job import Job
from hsabackend.models.quote import Quote
from hsabackend.models.discount_type import DiscountType
from hsabackend.models.invoice  import Invoice
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.subscription import Subscription
from django.utils import timezone
import traceback

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
            User.objects.create_user("testuser", "test@uiowa.edu", "SepTeam003!")
            usr  = User.objects.first()
            usr1  = User.objects.last()
            
            org = Organization.objects.create(
                org_name = "org",
                org_email = "org@org.dev",
                org_city = "Iowa City",
                org_requestor_state = "IA",
                org_requestor_zip = "52240",
                org_requestor_address = "123 main st",
                org_owner_first_name = "Dev",
                org_owner_last_name = "User",
                owning_User = usr
                )
            org.save()
            org1 = Organization.objects.create(
                org_name = "org1",
                org_email = "org1@org1.dev",
                org_city = "Iowa City",
                org_requestor_state = "IA",
                org_requestor_zip = "52240",
                org_requestor_address = "123 main st",
                org_owner_first_name = "Test",
                org_owner_last_name = "User",
                owning_User = usr1
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
                    first_name=f"First{i} testuser",
                    last_name=f"Last{i} testuser",
                    email=f"testuser{i}@example.com",
                    phone_no=f"{random.randint(1000000000, 9999999999)}",
                    notes=f"Sample notes for test user {i}",
                    organization=org1
                )
                c2.save()

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
                    "requestor_name": "John Doe",
                    "requestor_email": "johndoe@example.com",
                    "requestor_city": "New York",
                    "requestor_state": "NY",
                    "requestor_zip": "10001",
                    "requestor_address": "123 Main St",
                    "description": "Request for plumbing services due to a leaky faucet.",
                    "status": "received",
                },
                {
                    "requestor_name": "Jane Smith",
                    "requestor_email": "janesmith@example.com",
                    "requestor_city": "Los Angeles",
                    "requestor_state": "CA",
                    "requestor_zip": "90001",
                    "requestor_address": "456 Elm St",
                    "description": "Request for electrical repair for faulty wiring.",
                    "status": "approved",
                },
                {
                    "requestor_name": "Alice Johnson",
                    "requestor_email": "alicej@example.com",
                    "requestor_city": "Chicago",
                    "requestor_state": "IL",
                    "requestor_zip": "60601",
                    "requestor_address": "789 Oak St",
                    "description": "Request for HVAC maintenance before winter.",
                    "status": "received",
                },
                {
                    "requestor_name": "Bob Brown",
                    "requestor_email": "bobbrown@example.com",
                    "requestor_city": "Houston",
                    "requestor_state": "TX",
                    "requestor_zip": "77001",
                    "requestor_address": "101 Pine St",
                    "description": "Request for landscaping services for backyard renovation.",
                    "status": "received",
                },
                {
                    "requestor_name": "Charlie Davis",
                    "requestor_email": "charlied@example.com",
                    "requestor_city": "Phoenix",
                    "requestor_state": "AZ",
                    "requestor_zip": "85001",
                    "requestor_address": "202 Maple St",
                    "description": "Request for pest control due to ant infestation.",
                    "status": "approved",
                },
            ]
            for data in mock_requests:
                r = Request.objects.create(
                    requestor_name=data["requestor_name"],
                    requestor_email=data["requestor_email"],
                    requestor_city=data["requestor_city"],
                    requestor_state=data["requestor_state"],
                    requestor_zip=data["requestor_zip"],
                    requestor_address=data["requestor_address"],
                    description=data["description"],
                    status=data["status"],
                    organization=org,
                )
                r.save()

                r = Request.objects.create(
                    requestor_name=data["requestor_name"].split()[0] + " test",
                    requestor_email=data["requestor_email"],
                    requestor_city=data["requestor_city"],
                    requestor_state=data["requestor_state"],
                    requestor_zip=data["requestor_zip"],
                    requestor_address=data["requestor_address"],
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
                    job_status=random.choice(['created', 'completed']),
                    start_date=timezone.now().date(),
                    end_date=timezone.now().date() + timezone.timedelta(days=random.randint(1, 30)),
                    description=random.choice(job_descriptions),
                    organization=org,
                )
                j.save()

                j = Job.objects.create(
                    job_status=random.choice(['created', 'completed']),
                    start_date=timezone.now().date(),
                    end_date=timezone.now().date() + timezone.timedelta(days=random.randint(1, 30)),
                    description=random.choice(job_descriptions) + " test",
                    organization=org1,
                )
                j.save()


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

            for i in range(5):
                issuance_date = timezone.now().date()
                due_date = issuance_date + timezone.timedelta(days=30)
                status = 'created' if i % 2 == 0 else 'accepted'
                material_subtotal = 1000.0 * (i + 1)
                total_price = material_subtotal * 0.9  # 10% discount
                jobID = jobs_org_1[i]
                

                q = Quote.objects.create(
                    issuance_date=issuance_date,
                    due_date=due_date,
                    status=status,
                    material_subtotal=material_subtotal,
                    total_price=total_price,
                    jobID=jobID,
                    discount_type = random.choice(discounts_1)
                    )
                q.save()

                issuance_date = timezone.now().date()
                due_date = issuance_date + timezone.timedelta(days=30)
                status = 'created' if i % 2 == 0 else 'accepted'
                material_subtotal = 1000.0 * (i + 1)
                total_price = material_subtotal * 0.9  # 10% discount
                jobID = jobs_org[i]
                

                q = Quote.objects.create(
                    issuance_date=issuance_date,
                    due_date=due_date,
                    status=status,
                    material_subtotal=material_subtotal,
                    total_price=total_price,
                    jobID=jobID,
                    discount_type = random.choice(discounts)
                    )
                q.save()


        
            customers = Customer.objects.filter(organization=org.pk)
            customers_1 = Customer.objects.filter(organization=org.pk)


            for i in range(5):
                iv = Invoice.objects.create(
                    issuance_date=timezone.now().date(),
                    due_date=timezone.now().date() + timezone.timedelta(days=30),
                    status='issued',
                    price=100.0 * (i + 1),
                    customer=customers[i]
                )
                iv.save()

                iv = Invoice.objects.create(
                    issuance_date=timezone.now().date(),
                    due_date=timezone.now().date() + timezone.timedelta(days=30),
                    status='issued',
                    price=100.0 * (i + 1),
                    customer=customers_1[i]
                )
                iv.save()

            for i in range(5):
                j = JobTemplate.objects.create(
                    description=f"Job Template Description {i+1}",
                    organization=org)
                j.save()
                j = JobTemplate.objects.create(
                    description=f"Job Template Description {i+1}",
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
        