from behave import given, then, when
from selenium.webdriver.common.by import By

@given('I am on the customers page')
def step_given_user_on_customer_page(context):
    context.browser.get(f"{context.url}/customers")

@when('I fill in first name with "{fn}"')
def step_fill_in_first_name(context, fn):
    username_field = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="first-name-input"]')
    username_field.clear()
    username_field.send_keys(fn)

@when('I fill in last name with "{ln}"')
def step_fill_in_last_name(context, ln):
    username_field = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="last-name-input"]')
    username_field.clear()
    username_field.send_keys(ln)

@when('I fill in email with "{email}"')
def step_fill_in_email(context, email):
    username_field = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="email-input"]')
    username_field.clear()
    username_field.send_keys(email)

@when('I fill in phone with "{phone}"')
def step_fill_in_phone(context, phone):
    username_field = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="phone-input"]')
    username_field.clear()
    username_field.send_keys(phone)

@when('I click the submit button')
def click_submit(context):
    submit_button = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="submit"]')
    submit_button.click()

