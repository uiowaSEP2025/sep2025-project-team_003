from behave import   then
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
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "simple-snack-bar")))
    assert text in element.text, f"Snack bar doesn't contain '{text}'"