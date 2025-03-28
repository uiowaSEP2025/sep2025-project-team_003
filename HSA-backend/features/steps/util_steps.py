from behave import   then
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


@then(u'I wait for {n} sec')
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
    element = context.driver.find_element(By.TAG_NAME, "simple-snack-bar")
    assert text in element.text, f"Snack bar doesn't contain '{text}'"