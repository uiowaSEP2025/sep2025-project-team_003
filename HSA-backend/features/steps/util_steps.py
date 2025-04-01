from behave import then, given, when
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

@then(u'I wait for {n} seconds')
def step_wait_n_seconds(context, n):
    """This makes the browser freeze for n secs. use for debugging"""
    try:
        WebDriverWait(context.browser, float(n)).until(
            lambda _: False  
        )
    except:
        pass  

@then('I should see a snackbar with "{text}"')
def step_check_snackbar_text(context, text):
    wait = WebDriverWait(context.browser, 20)
    element = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "simple-snack-bar")))
    assert text in element.text, f"Snack bar doesn't contain '{text}'"

@given('I am logged in')
def step_user_logged_in(context):
    context.browser.get(f"{context.url}/login")

    username_field = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="username-input"]')
    username_field.clear()
    username_field.send_keys("devuser")

    password_field = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="password-input"]')
    password_field.clear()
    password_field.send_keys("SepTeam003!")

    submit_button = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="submit"]')
    submit_button.click()

    text = "Login Successful"
    wait = WebDriverWait(context.browser, 20)
    element = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "simple-snack-bar")))
    assert text in element.text, f"Snack bar doesn't contain '{text}'"

@then('I {should_or_not} see a table row with the following elements')
def find_rows(context, should_or_not):
    should_or_not = should_or_not == 'should'
    expected_values = [row[0] for row in context.table]  # Extract expected values
    rows = context.browser.find_elements(By.CSS_SELECTOR, "table tr")
    
    found = False
    for row in rows:
        print(row)
        cells = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if all(value in cells for value in expected_values):  # Check if all expected values exist in the row
            found = True
            break  # No need to continue once we find a matching row
    
    assert should_or_not == found, f"{'No table ' if should_or_not else 'Table '}row found containing values: {expected_values}"

@when('I click the delete button')
def set_click_delete(context):
    rows = context.browser.find_elements(By.TAG_NAME, "tr")
    second_row = rows[1]
    print(rows)
    buttons = second_row.find_elements(By.TAG_NAME, "mat-icon")
    found = False
    for button in buttons:
        if button.text.strip().lower() == "delete":
            found = True
            button.click()
    assert found, "Did not find the delete button"

@when('I don\'t see the loading spinner')
def await_not_showing_spinner(context):
    # Wait until the element with class "lds-roller" is no longer visible
    WebDriverWait(context.browser, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "lds-roller"))
    )

@when('I confirm the delete dialog')
def step_confirm_delete_dialog(context):
    wait = WebDriverWait(context.browser, 10)
    
    # Find the delete confirmation dialog
    dialog = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "mat-mdc-dialog-surface"))
    )
    assert dialog is not None, "Delete confirmation dialog not found"

    # Find and click the Delete button
    delete_button = wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, "delete-button"))
    )
    delete_button.click()

@then('I should see "Nothing to show here" in the table')
def step_look_for_empty_table(context):
    # Wait for the table to be visible
    table = WebDriverWait(context.browser, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "app-table-component"))
    )

    # Get all child elements of the table
    child_elements = table.find_elements(By.XPATH, ".//*")

    # Check if any child element contains the expected text
    assert any("Nothing to show here" in child.text for child in child_elements), \
        'Expected text "Nothing to show here" not found in table'
    
@when('I click the edit button')
def step_click_edit(context):
    rows = context.browser.find_elements(By.TAG_NAME, "tr")
    second_row = rows[1]
    buttons = second_row.find_elements(By.TAG_NAME, "mat-icon")
    found = False
    for button in buttons:
        if button.text.strip().lower() == "edit":
            found = True
            button.click()
            break # avoid stale element exception
    assert found, "Did not find the edit button"

@when('I click the first table row')
def step_click_table_row(context):
    rows = context.browser.find_elements(By.TAG_NAME, "tr")
    second_row = rows[1]
    second_row.click()

@when('I click the submit button')
def click_submit(context):
    submit_button = context.browser.find_element(By.CSS_SELECTOR, '[data-testid="submit"]')
    submit_button.click()