from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from models import *
from django.contrib.auth.models import User

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
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding the database: {e}'))
        