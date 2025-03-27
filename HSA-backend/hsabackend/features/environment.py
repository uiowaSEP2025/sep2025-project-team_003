import subprocess
import time
import os
import requests
from requests.exceptions import ConnectionError
import time
from selenium import webdriver
import psycopg2
from django.core.management import call_command
import django
import sys
import signal

def kill_all_connections():
    """we need this or we can't run the flush command or we can't drop or flush the database
    idk what's causing the connection not to be released"""
    connection = psycopg2.connect(database="postgres", 
                                  user=os.environ["DATABASE_USERNAME"], 
                                  password=os.environ["DATABASE_PASSWORD"], 
                                  host=os.environ["DATABASE_IP"], port=5432)
    
    connection.autocommit = True
    cursor = connection.cursor()
    connection.autocommit = True
    cursor.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'hsatest';")
    
    cursor.close()
    connection.close()

def block_until_server_is_up(url, timeout=30, interval=2):
    """Block until the server is up."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.ok:
                return True
        except ConnectionError:
            pass
        time.sleep(interval)
    return False

def before_scenario(context, scenario):
    kill_all_connections()
    call_command('seedint') # clears the database between runs
    

def before_all(context):
    """If runing on CICD ```behave -D CI=True```"""
    context.is_CI = context.config.userdata.get("CI", False)
    context.is_dev = context.config.userdata.get("DEV", False) # if the integration tests are being ran against dev
    context.browser = webdriver.Chrome()
    context.url = "http://localhost:4200" if not context.is_dev else "TODO: FIX IT PLEASE"

    connection = psycopg2.connect(database="postgres", 
                                  user=os.environ["DATABASE_USERNAME"], 
                                  password=os.environ["DATABASE_PASSWORD"], 
                                  host=os.environ["DATABASE_IP"], port=5432)
    
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS hsatest;")
    cursor.execute("CREATE DATABASE hsatest;")

    os.environ["DATABASE_NAME"] = "hsatest"

    cursor.close()
    connection.close()

    if context.is_CI:
        pass
    else:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../HSA-frontend')) # frontend to do ng serve
        os.chdir(path)
        context.angular_process = subprocess.Popen(["ng", "serve", "--port", "4200"])
        block_until_server_is_up("http://localhost:4200")
        
        if context.angular_process.poll() is not None:
            error_message = "Angular server failed to start. \n"
            if context.angular_process.returncode == 0:
                error_message += "Process exited successfully but shouldn't have.\n"
            else:
                error_message += f"Process exited with return code {context.server_process.returncode} \n"
            raise RuntimeError(error_message)
        print("Angular was started successfully")
        
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')) # frontend to do ng serve
    os.chdir(path)
    sys.path.append(path) # we need this so python can find our app as a module
    
    os.environ["DJANGO_SETTINGS_MODULE"] =  "hsabackend.settings"
    django.setup()  # This initializes Django

    call_command('migrate', interactive=False)
    context.django_process = subprocess.Popen(["python3", "manage.py", "runserver"])
    block_until_server_is_up("http://localhost:8000/api/healthcheck")
    
    if context.django_process.poll() is not None:
        error_message = "Django failed to start. \n"
        if context.server_process.returncode == 0:
            error_message += "Process exited successfully but shouldn't have.\n"
        else:
            error_message += f"Process exited with return code {context.server_process.returncode} \n"
        raise RuntimeError(error_message)
    print("Django was started successfully")


def after_all(context):
    if context.is_CI:
        pass
    else:
        context.angular_process.kill()
        context.angular_process.wait()
        
    # WARNING, THIS NEEDS TO BE SIGINT OR DJANGO WILL NOT CLEAN UP PROPERLY. I HAVE SPENT 2 HOURS SOLVING THIS!!!!. DO NOT
    # CHANGE THE NEXT LINE. YOU HAVE BEEN WARNED!!!!!!!!
    context.django_process.send_signal(signal.SIGINT)
    context.django_process.wait()
    print(context.django_process.poll(), "djoango killed with")
    print("About to drop the test database")
    connection = psycopg2.connect(database="postgres", 
                                  user=os.environ["DATABASE_USERNAME"], 
                                  password=os.environ["DATABASE_PASSWORD"], 
                                  host=os.environ["DATABASE_IP"], port=5432)
    
    connection.autocommit = True
    cursor = connection.cursor()
    kill_all_connections()
    cursor.execute("DROP DATABASE IF EXISTS hsatest;")
    cursor.close()
    connection.close()
    