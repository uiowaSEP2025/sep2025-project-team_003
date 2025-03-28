from behave import given, when
from selenium.webdriver.common.by import By

@given('I am on the login page')
def step_given_user_on_login_page(context):
    context.browser.get(f"{context.url}/login")

@when('I type "{text}" into the username field')
def type_into_username(context, text):
    # Find the element by data-test-id and type the text
    username_field = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="username-input"]')
    username_field.clear()
    username_field.send_keys(text)

@when('I type "{text}" into the password field')
def type_into_password(context, text):
    # Find the element by data-test-id and type the text
    username_field = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]')
    username_field.clear()
    username_field.send_keys(text)

@when('I click the submit button')
def click_submit(context):
    submit_button = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="submit"]')
    submit_button.click()
