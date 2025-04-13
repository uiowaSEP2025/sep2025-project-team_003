from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@given('I am on the onboarding page')
def step_given_user_on_customer_page(context):
    context.browser.get(f"{context.url}/onboarding")

@when(u'I type on the {text_field} with {text}')
def type_input_field(context, text_field, text):
    input_field = context.browser.find_element(By.CSS_SELECTOR, f'[data-testid={"-".join(text_field.replace("*", "").lower().split(" "))}]')
    input_field.location_once_scrolled_into_view
    input_field.clear()
    input_field.send_keys(text)

@when(u'I click the {button} button')
def click_button(context, button):
    button = context.browser.find_element(By.CSS_SELECTOR, f'[data-testid={"-".join(str(button).lower().split(" "))}]')
    button.location_once_scrolled_into_view
    button.click()

@when(u'I select any option')
def click_button(context):
    option = context.browser.find_element(By.CSS_SELECTOR, f'[data-testid="option"]')
    option.location_once_scrolled_into_view
    option.click()

@then(u'I expect the input field {text_field} show up')
def expect_input_field(context, text_field):
    wait = WebDriverWait(context.browser, 10)
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid={"-".join(text_field.replace("*", "").lower().split(" "))}]')))
    element.location_once_scrolled_into_view

@then(u'I expect the button {button} show up')
def expect_input_field(context, button):
    wait = WebDriverWait(context.browser, 10)
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid={"-".join(button.lower().split(" "))}]')))
    element.location_once_scrolled_into_view