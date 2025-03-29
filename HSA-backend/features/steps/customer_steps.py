from behave import given, then, when
from selenium.webdriver.common.by import By

@given('I am on the customers page')
def step_given_user_on_customer_page(context):
    context.browser.get(f"{context.url}/customers")

