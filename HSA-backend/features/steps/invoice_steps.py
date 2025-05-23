from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


@given('I am on the invoices page')
def step_given_user_on_customer_page(context):
    context.browser.get(f"{context.url}/invoices")

@then('I should see the info table with the following data')
def step_check_invoice_info(context):
    """WARNING: Behave will always ignore the first row becuaase it's a header. 
    need to pass a dummy 1st row for it to work
    """
    wait = WebDriverWait(context.browser, 10)
    table = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="info-table"]'))
    )
    expected_values = [list(row) for row in context.table]
    rows = table.find_elements(By.TAG_NAME, "tr")
    actual_values = [
        [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, "td")]
        for row in rows
    ]
    assert expected_values == actual_values, f"Expected {expected_values}, but got {actual_values}"

@then('I should see the cost table with the following data')
def step_check_invoice_info(context):
    """WARNING: Behave will always ignore the first row becuaase it's a header. 
    need to pass a dummy 1st row for it to work
    """
    expected_values = [list(row) for row in context.table]
    table = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="cost-table"]')
    rows = table.find_elements(By.TAG_NAME, "tr")
    actual_values = [
        [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, "td")]
        for row in rows]
    actual_values = actual_values[1:] # removing the table header
    assert expected_values == actual_values, f"Expected {expected_values}, but got {actual_values}"

@when('I select a status with "{n}"')
def step_select_invoice_status(context, n):
    selector = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="status-selector"]')
    selector.click()
    
    # Wait for the dropdown options to appear
    option = WebDriverWait(context.browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, f'//mat-option[@value="{n}"]'))
    )
    option.click()

@when('I fill in the dates with "{d1}" and "{d2}"')
def step_fill_in_dates(context, d1, d2):
    wait = WebDriverWait(context.browser, 10)
    dates = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="date-picker"]'))
    )
    inputs = dates.find_elements(By.TAG_NAME, "input")
    start, end = inputs[0], inputs[1]
    for i in range(10):                 # calling .clear does not work on date pickers
        start.send_keys(Keys.BACKSPACE)
    start.send_keys(d1)
    for i in range(10):
        end.send_keys(Keys.BACKSPACE)
    end.send_keys(d2)

@when('I click the first checkbox in the invoice quotes table')
def step_click_first_checkbox_invoice_quotes(context):
    wait = WebDriverWait(context.browser, 10)
    table = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="invoice-quotes-table"]'))
    )
    row1 = table.find_elements(By.TAG_NAME, "tr")[1]  # Assuming the first row is the header
    checkbox = row1.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
    checkbox.click()

@when('I click the first checkbox in the invoice customer table')
def step_click_first_checkbox_invoice_quotes(context):
    wait = WebDriverWait(context.browser, 10)
    table = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="invoice-customers-table"]'))
    )
    row1 = table.find_elements(By.TAG_NAME, "tr")[1]  # Assuming the first row is the header
    checkbox = row1.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
    checkbox.click()

@when('I fill in the tax rate with "{n}"')
def step_fill_in_tax_rate(context,n):
    wait = WebDriverWait(context.browser, 10)
    tax_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tax-input"]'))
    )
    tax_input.clear()
    tax_input.send_keys(n)

@when('I confirm the edit')
def step_invoice_confirmation(context):
    wait = WebDriverWait(context.browser, 10)
    confirmation_dialog = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tax-input"]'))
    )
    confirm_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="confirm-button"]'))
    )
    confirm_button.click()

@when('I click the create invoice button')
def step_click_create_invoice(context):
    wait = WebDriverWait(context.browser, 10)
    confirm_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="create-button"]'))
    )
    confirm_button.click()
    