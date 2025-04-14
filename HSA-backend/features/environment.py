import os
from selenium import webdriver
import sys
import subprocess
import signal
import time
import requests
import traceback
from behave import fixture, use_fixture
from django.core.management import call_command
from django.core.management.base import CommandError
import os

def block_for_server(url):
     # Wait for Angular to be ready
        max_attempts = 30
        attempt = 0
        success = False
        
        while attempt < max_attempts and not success:
            attempt += 1
            try:
                # Try to access the development server
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    success = True
                else:
                    time.sleep(1)
            except (requests.exceptions.ConnectionError, requests.exceptions.RequestException):
                time.sleep(1)
                print(f"Waiting for {url}. {attempt}/{max_attempts}")
        if not success:
            raise RuntimeError(f'Timed out waiting for {url}')
        

@fixture
def django_server(context):
    # Start Django dev server in the background on port 8000
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../HSA-backend'))
    os.chdir(path)
    os.environ["DATABASE_NAME"] = "hsaint"

    if os.name == 'nt':
        context.django = subprocess.Popen("python manage.py runserver 8000", shell=True)
    else:
        context.django = subprocess.Popen(["python", "manage.py", "runserver", "8000"])
    
    block_for_server("http://localhost:8000/api/healthcheck")
    yield
    # Stop server after tests
    context.django.terminate()
    context.django.wait()

def before_scenario(context, scenario):
    """Run before each scenario."""
    try:
        print('\n\n\n')
        call_command('seedint') # truncates all tables
    except CommandError as e:
        print(f'Error flushing the database: {e}')

def before_all(context):
    try:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        sys.path.append(path)  # we need this so python can find our app as a module
        os.environ["DJANGO_SETTINGS_MODULE"] = "hsabackend.settings"
        if "INTEGRATION_FLAG" in os.environ:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')  # Run in headless mode
            chrome_options.add_argument('--disable-gpu')  # Disable GPU usage (often recommended)
            chrome_options.add_argument('--window-size=1920,1080')  # Set a binary size (if needed)
            chrome_options.add_argument('--no-sandbox')  # (Optional) May help in some CI environments
            chrome_options.add_argument('--disable-dev-shm-usage')  # (Optional) Overcome limited resource problems
            context.url = "http://localhost:8000"
            try:
                context.browser = webdriver.Chrome(options=chrome_options)
            except Exception as e:
                print(f"Error creating WebDriver: {e}")
                raise
        else:
            print("CONTEXT IGNORED, Integration flag value was not set.")
            context.url = "http://localhost:4200"
            path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../HSA-frontend'))
            os.chdir(path)
            if os.name == 'nt':
                context.angular = subprocess.Popen("ng serve", shell=True)
            else:
                context.angular = subprocess.Popen(["ng", "serve"])
            
            block_for_server("http://localhost:4200")
            context.browser = webdriver.Chrome()
        use_fixture(django_server, context)  # Start server before all scenarios
        
    except Exception as e:
            stack_trace = traceback.format_exc()
            print("Took an exception in the before all hook")
            print(stack_trace)
        

def after_all(context):
    if "INTEGRATION_FLAG" in os.environ:
        context.browser.quit()
    else:
        context.angular.send_signal(signal.SIGINT)
        context.angular.wait()