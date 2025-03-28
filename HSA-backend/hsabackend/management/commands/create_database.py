from django.core.management.base import BaseCommand
from django.db import connection
import sys


class Command(BaseCommand):
    help = 'Creates the database specified in settings.py'

    def handle(self, *args, **options):
        db_settings = connection.settings_dict
        db_name = db_settings['NAME']
        
        self.stdout.write(f"Attempting to create database '{db_name}'...")
        
        try:
            # Create a temporary connection without specifying the database
            from django.db import connections
            temp_connection = connections['default']
            temp_connection.settings_dict['NAME'] = None
            cursor = temp_connection.cursor()
            
            # Try to create the database
            cursor.execute(f"CREATE DATABASE {db_name}")
            self.stdout.write(self.style.SUCCESS(f"Successfully created database '{db_name}'"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating database: {e}"))
            sys.exit(1)