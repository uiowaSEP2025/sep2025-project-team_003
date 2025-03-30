from behave import given, then
from selenium.webdriver.common.by import By

@given('I am on the invoices page')
def step_given_user_on_customer_page(context):
    context.browser.get(f"{context.url}/invoices")

@then('I should see the info table with the following data')
def step_check_invoice_info(context):
    """WARNING: Behave will always ignore the first row becuaase it's a header. 
    need to pass a dummy 1st row for it to work
    """
    expected_values = [list(row) for row in context.table]
    table = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="info-table"]')
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