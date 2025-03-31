from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import traceback
from django.contrib.auth.models import User
from hsabackend.models.organization import Organization
from hsabackend.models.customer import Customer

def add_users():
    User.objects.create_user("devuser", "dev@uiowa.edu", "SepTeam003!")
    User.objects.create_user("testuser", "test@uiowa.edu", "SepTeam003!")
    usr  = User.objects.first()
    usr1  = User.objects.last()
    return usr,usr1

def add_orgs(u1,u2):
    org = Organization.objects.create(
        org_name = "devorg",
        org_email = "org@org.dev",
        org_city = "Iowa City",
        org_requestor_state = "Iowa",
        org_requestor_zip = "52240",
        org_requestor_address = "123 main st",
        org_owner_first_name = "Dev",
        org_owner_last_name = "User",
        owning_User = u1,
        org_phone = "1234567890"
        )
    org1 = Organization.objects.create(
        org_name = "testorg",
        org_email = "org1@org1.dev",
        org_city = "Iowa City",
        org_requestor_state = "Iowa",
        org_requestor_zip = "52240",
        org_requestor_address = "123 main st",
        org_owner_first_name = "Test",
        org_owner_last_name = "User",
        owning_User = u2,
        org_phone = "1234567890"
        )
    return org,org1

def add_customers(org1,org2):
    c1 = Customer.objects.create(
        first_name=f"Firstorg1",
        last_name=f"Lastorg1",
        email=f"custorg1@example.com",
        phone_no=f"1234567890",
        notes=f"Sample notes for user customer org1",
        organization=org1
    )
    c2 = Customer.objects.create(
        first_name=f"Firstorg2",
        last_name=f"Lastorg2",
        email=f"custorg1@example.com",
        phone_no=f"0987654321",
        notes=f"Sample notes for user customer org2",
        organization=org2
    )
    return c1,c2


class Command(BaseCommand):
    """Seeds the database with deterministic test data. Used for integration tests"""

    def handle(self, *args, **options):
        try:
            call_command('flush', interactive=False) # truncates all tables
            self.stdout.write(self.style.SUCCESS('Database flushed successfully'))
        except CommandError as e:
            self.stdout.write(self.style.ERROR(f'Error flushing the database: {e}'))
        try:
            u1,u2 = add_users()
            o1,o2 = add_orgs(u1,u2)
            c1,c2 = add_customers(o1,o2)
            
        except Exception as e:
            stack_trace = traceback.format_exc()
            self.stdout.write(self.style.ERROR(f'Error seeding the database: {e}\n{stack_trace}'))
        