# -- FILE: my_django/behave_fixtures.py
from behave import fixture
from behave import use_fixture
from django.test.testcases import LiveServerTestCase
import os
from selenium import webdriver
import sys
import django
import subprocess
from django.core.management import call_command

@fixture
def django_test_case(context):
    context.test_case = LiveServerTestCase
    context.test_case.port = 8000
    context.test_case.setUpClass()
    yield
    context.test_case.tearDownClass()
    del context.test_case

def before_all(context):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sys.path.append(path) # we need this so python can find our app as a module
    os.environ["DJANGO_SETTINGS_MODULE"] = "hsabackend.settings"
    context.url = "localhost:8000"
    os.environ["DATABASE_NAME"] = "hsaint"
    context.browser = webdriver.Chrome()

    django.setup()
    call_command("create_database")
    use_fixture(django_test_case, context)

def after_all(context):
    call_command('drop_database', interactive=False)
