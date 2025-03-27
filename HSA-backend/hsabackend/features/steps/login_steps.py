from behave import given, when, then
from selenium import webdriver
import time

@given('I am on the login page')
def step_given_user_on_login_page(context):
    context.browser = webdriver.Chrome()
    print(f"{context.url}/login")
    context.browser.get(f"{context.url}/login")


