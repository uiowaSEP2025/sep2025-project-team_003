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
from hsabackend.models.quote import Quote
from hsabackend.models.discount_type import DiscountType
from hsabackend.models.job_template import JobTemplate
from hsabackend.models.subscription import Subscription
from django.utils import timezone
import traceback
from hsabackend.models.job_material import JobMaterial




class Command(BaseCommand):
    """Seeds the database with deterministic test data. Used for integration tests"""

    def handle(self, *args, **options):
        try:
            call_command('flush', interactive=False) # truncates all tables
            self.stdout.write(self.style.SUCCESS('Database flushed successfully'))
        except CommandError as e:
            self.stdout.write(self.style.ERROR(f'Error flushing the database: {e}'))
        try:
            pass

        except Exception as e:
            stack_trace = traceback.format_exc()
            self.stdout.write(self.style.ERROR(f'Error seeding the database: {e}\n{stack_trace}'))
        