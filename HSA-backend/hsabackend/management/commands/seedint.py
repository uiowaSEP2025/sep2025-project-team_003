from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import traceback
from django.contrib.auth.models import User

def add_users():
    User.objects.create_user("devuser", "dev@uiowa.edu", "SepTeam003!")
    User.objects.create_user("testuser", "test@uiowa.edu", "SepTeam003!")

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
        