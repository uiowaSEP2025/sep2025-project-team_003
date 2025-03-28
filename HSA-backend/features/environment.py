import os
from selenium import webdriver
import sys
import subprocess
import signal
import time
import requests
import traceback
from behave import fixture, use_fixture


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
                    print("Angular dev server is ready!")
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
    print(path, 'pathhhhhhh')
    context.django = subprocess.Popen(["python", "manage.py", "runserver", "8000"])
    print(context.django.poll())
    block_for_server("http://localhost:8000/api/healthcheck")
    yield
    # Stop server after tests
    context.django.terminate()
    context.django.wait()


def before_all(context):
    try:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        sys.path.append(path) # we need this so python can find our app as a module
        os.environ["DJANGO_SETTINGS_MODULE"] = "hsabackend.settings"
        context.url = "http://localhost:4200"
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../HSA-frontend'))
        os.chdir(path)
        context.angular = subprocess.Popen(["ng", "serve"])
        block_for_server("http://localhost:4200")
        context.browser = webdriver.Chrome()
        use_fixture(django_server, context)  # Start server before all scenarios
        
    except Exception as e:
            stack_trace = traceback.format_exc()
            print("Took an exception in the before all hook")
            print(stack_trace)
        

def after_all(context):
    context.angular.send_signal(signal.SIGINT)
    context.angular.wait()