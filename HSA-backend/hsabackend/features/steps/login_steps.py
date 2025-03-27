from behave import given, when
from selenium import webdriver
from selenium.webdriver.common.by import By

@given('I am on the login page')
def step_given_user_on_login_page(context):
    context.browser = webdriver.Chrome()
    print(f"{context.url}/login")
    context.browser.get(f"{context.url}/login")

@when('I type "{text}" into the username field')
def type_into_username(context, text):
    # Find the element by data-test-id and type the text
    username_field = context.browser.find_element(By.CSS_SELECTOR, '[data-test-id="username"]')
    username_field.clear()
    username_field.send_keys(text)