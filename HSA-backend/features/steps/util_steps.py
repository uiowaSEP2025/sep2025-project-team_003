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
    wait = WebDriverWait(context.browser, 5)
    # Wait for the text to appear within the div element
    element = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.mat-mdc-snack-bar-label"))
    )
    context.browser.execute_script("alert('shit')")

    assert element is not None, "SnackBar was not found"
    assert text in element.text, f"SnackBar doesn't contain '{text}', text was '{element.text}'"

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
    wait = WebDriverWait(context.browser, 5)
    # Wait for the text to appear within the div element
    element = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div.mat-mdc-snack-bar-label"))
    )
    wait.until(EC.text_to_be_present_in_element(element, text))
    assert element is not None, "SnackBar was not found"
    assert text in element.text, f"SnackBar doesn't contain '{text}', text was '{element.text}'"

@then('I {should_or_not} see a table row with the following elements')
def find_rows(context, should_or_not):
    should_or_not = should_or_not == 'should'
    expected_values = [row[0] for row in context.table]  # Extract expected values
    rows = context.browser.find_elements(By.CSS_SELECTOR, "table tr")
    
    found = False
    for row in rows:
        cells = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if all(value in cells for value in expected_values):  # Check if all expected values exist in the row
            found = True
            print('foint it')
            break  # No need to continue once we find a matching row
    
    assert should_or_not == found, f"{'No table ' if should_or_not else 'Table '}row found containing values: {expected_values}"

@when('I click the delete button')
def set_click_delete(context):
    rows = context.browser.find_elements(By.TAG_NAME, "tr")
    second_row = rows[0]
    buttons = second_row.find_elements(By.TAG_NAME, "mat-icon")
    found = False
    for button in buttons:
        print(button.text.strip().lower(), 'asdfa')
        if button.text.strip().lower() == "delete":
            found = True
            button.click()
    assert found, "Did not find the delete button"