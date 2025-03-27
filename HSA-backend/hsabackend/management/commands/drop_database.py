from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command
import sys
import os

class Command(BaseCommand):
    help = 'Drops the database specified in settings.py'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false',
            dest='interactive',
            help='Tells Django to NOT prompt the user for input of any kind.',
        )

    def handle(self, *args, **options):
        db_name = os.environ["DATABASE_NAME"]
        
        self.stdout.write(f"Attempting to drop database '{db_name}'...")
        
        # Skip confirmation if --noinput is passed
        if options['interactive']:
            confirm = input(f"Are you sure you want to drop database '{db_name}'? This cannot be undone. (yes/no): ")
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING("Database drop cancelled."))
                return

        try:
            # First flush the database to clear all data
            self.stdout.write("Flushing database contents...")
            call_command('flush', interactive=False)
            
            # Create a temporary connection without specifying the database
            from django.db import connections
            temp_connection = connections['default']
            temp_connection.settings_dict['NAME'] = None
            cursor = temp_connection.cursor()
            
            # Try to drop the database
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            self.stdout.write(self.style.SUCCESS(f"Successfully dropped database '{db_name}'"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error dropping database: {e}"))
            sys.exit(1)